"""RPM-related classes and procedures."""

import operator
import re
from functools import partialmethod
from pathlib import Path
from typing import BinaryIO, Callable, Tuple, TypeVar, Union

import attr
from attr.validators import instance_of, optional

from .util import system_import

_rpm = system_import("rpm")

# type aliases for comparison functions
CompareOperator = Callable[[TypeVar("T"), TypeVar("T")], bool]
CompareResult = Union[bool, type(NotImplemented)]


# NEVRA-related regular expressions
EPOCH_RE = re.compile(r"(\d+):")
NVRA_re = re.compile(
    r"""
    ^
    (?P<name>\S+)-          # package name
    (?P<version>[\w.]+)-    # package version
    (?P<release>\w+(?:\.[\w+]+)+?)  # package release, with required dist tag
    (?:\.(?P<arch>\w+))?    # optional package architecture
    (?:\.rpm)??             # optional rpm extension
    $
""",
    flags=re.VERBOSE,
)
# .el7_4 format
LONG_DIST_RE = re.compile(
    r"""
    (\.         # short dist tag starts with a dot…
    [^\W\d_]+   # … followed by at least one letter…
    \d+)        # … and ended by at least one digit
    [^.]*  # any other characters up to the next dot
""",
    flags=re.VERBOSE,
)


# Helper for ensuring resolved paths
def _resolve_path(path: Union[str, Path]) -> Path:
    """Resolve the path argument"""

    return Path(path).resolve()


@attr.s(slots=True, cmp=False, frozen=True, hash=True)
class Metadata:
    """Generic RPM metadata.

    This class should act as a basis for all the RPM-like objects,
    providing common comparison and other "dunder" methods.
    """

    #: RPM name
    name = attr.ib(validator=instance_of(str))
    #: RPM version
    version = attr.ib(validator=instance_of(str))
    #: RPM release
    release = attr.ib(validator=instance_of(str))

    #: Optional RPM epoch
    epoch = attr.ib(
        validator=optional(instance_of(int)),
        default=0,
        # special case for None: treat that as 0
        converter=lambda val: 0 if val is None else int(val),
    )

    #: RPM architecture
    arch = attr.ib(
        validator=optional(instance_of(str)),
        default="src",
        converter=lambda val: "src" if val is None else str(val),
    )

    # Alternative constructors

    @classmethod
    def from_file(cls, file: BinaryIO) -> "Metadata":
        """Read metadata from an RPM file.

        Keyword arguments:
            file: The IO object to read the metadata from.
                It has to provide a file descriptor – in-memory
                files are unsupported.

        Returns:
            New instance of Metadata.
        """

        transaction = _rpm.TransactionSet()
        # Ignore missing signatures warning
        transaction.setVSFlags(_rpm._RPMVSF_NOSIGNATURES)

        header = transaction.hdrFromFdno(file.fileno())

        # Decode the attributes
        attributes = {
            "name": header[_rpm.RPMTAG_NAME].decode("utf-8"),
            "version": header[_rpm.RPMTAG_VERSION].decode("utf-8"),
            "release": header[_rpm.RPMTAG_RELEASE].decode("utf-8"),
            "epoch": header[_rpm.RPMTAG_EPOCHNUM],
        }

        # For source RPMs the architecture reported is a binary one
        # for some reason
        if header[_rpm.RPMTAG_SOURCEPACKAGE]:
            attributes["arch"] = "src"
        else:
            attributes["arch"] = header[_rpm.RPMTAG_ARCH].decode("utf-8")

        return cls(**attributes)

    @classmethod
    def from_nevra(cls, nevra: str) -> "Metadata":
        """Parse a string NEVRA and converts it to respective fields.

        Keyword arguments:
            nevra: The name-epoch:version-release-arch to parse.

        Returns:
            New instance of Metadata.
        """

        arguments = {}

        # Extract the epoch, if present
        def replace_epoch(match):
            arguments["epoch"] = match.group(1)
            return ""

        nvra = EPOCH_RE.sub(replace_epoch, nevra, count=1)

        # Parse the rest of the string
        match = NVRA_re.match(nvra)
        if not match:
            message = "Invalid NEVRA string: {}".format(nevra)
            raise ValueError(message)

        arguments.update(match.groupdict())

        return cls(**arguments)

    # Derived attributes

    @property
    def nvr(self) -> str:
        """:samp:`{name}-{version}-{release}` string of the RPM object"""

        return "{s.name}-{s.version}-{s.release}".format(s=self)

    @property
    def nevra(self) -> str:
        """:samp:`{name}-{epoch}:{version}-{release}.{arch}` string of the RPM object"""

        return "{s.name}-{s.epoch}:{s.version}-{s.release}.{s.arch}".format(s=self)

    @property
    def label(self) -> Tuple[int, str, str]:
        """Label compatible with RPM's C API."""

        return (str(self.epoch), self.version, self.release)

    @property
    def canonical_file_name(self):
        """Canonical base file name of a package with this metadata."""

        if self.epoch:
            format = "{s.name}-{s.epoch}:{s.version}-{s.release}.{s.arch}.rpm"
        else:
            format = "{s.name}-{s.version}-{s.release}.{s.arch}.rpm"

        return format.format(s=self)

    # Comparison methods
    def _compare(
        self, other: "Metadata", oper: CompareOperator
    ) -> CompareResult:  # noqa: E501
        """Generic comparison of two RPM-like objects.

        Keyword arguments:
            other: The object to compare with
            oper: The operator to use for the comparison.

        Returns:
            bool: The result of the comparison.
            NotImplemented: Incompatible operands.
        """

        try:
            if self.name == other.name:
                return oper(_rpm.labelCompare(self.label, other.label), 0)
            else:
                return oper(self.name, other.name)

        except AttributeError:
            return NotImplemented

    __eq__ = partialmethod(_compare, oper=operator.eq)
    __ne__ = partialmethod(_compare, oper=operator.ne)
    __lt__ = partialmethod(_compare, oper=operator.lt)
    __le__ = partialmethod(_compare, oper=operator.le)
    __gt__ = partialmethod(_compare, oper=operator.gt)
    __ge__ = partialmethod(_compare, oper=operator.ge)

    # String representations
    def __str__(self) -> str:
        return self.nevra


@attr.s(slots=True, frozen=True, hash=True, cmp=False)
class LocalPackage(Metadata):
    """Metadata of existing RPM package on local file system."""

    #: Resolved path to the RPM package
    path = attr.ib(converter=_resolve_path)

    @path.default
    def pkg_in_cwd(self):
        """Canonically named package in current directory"""

        return Path.cwd() / self.canonical_file_name

    @path.validator
    def _existing_file_path(self, _attribute, path):
        """The path must point to an existing file"""

        if not path.is_file():
            raise FileNotFoundError(path)

    # Alternative constructors
    @classmethod
    def from_path(cls, path: Path) -> "LocalPackage":
        """Read metadata for specified RPM file path.

        Keyword arguments:
            path: The path to the file to read metadata for.

        Returns:
            New instance of LocalPackage.
        """

        with path.open(mode="rb") as file:
            metadata = attr.asdict(Metadata.from_file(file))

        return cls(**metadata, path=path)

    # Path-like protocol
    def __fspath__(self) -> str:
        return str(self.path)

    # String representation
    def __str__(self):
        return self.__fspath__()


# Utility functions
def shorten_dist_tag(metadata: Metadata) -> Metadata:
    """Shorten release string by removing extra parts of dist tag.

    Examples:
        - abcde-1.0-1.el7_4 → abcde-1.0-1.el7
        - binutils-3.6-4.el8+4 → binutils-3.6-4.el8
        - abcde-1.0-1.fc27 → abcde-1.0-1.fc27

    Keyword arguments:
        metadata: The metadata to shorten.

    Returns:
        Potentially modified metadata.
    """

    return attr.evolve(metadata, release=LONG_DIST_RE.sub(r"\1", metadata.release))
