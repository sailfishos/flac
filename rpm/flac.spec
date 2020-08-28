Name:          flac
Summary:       An encoder/decoder for the Free Lossless Audio Codec
Version:       1.3.3
Release:       0
License:       BSD and GPLv2+ and GFDL
URL:           https://xiph.org/flac/
Source:        %{name}-%{version}.tar.bz2
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gettext-devel
BuildRequires: pkgconfig(ogg)
%ifarch %{ix86}
# 2.0 supports symbol visibility
BuildRequires: nasm >= 2.0
%endif

%description
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, FLAC
is similar to Ogg Vorbis, but lossless. The FLAC project consists of
the stream format, reference encoders and decoders in library form,
flac, a command-line program to encode and decode FLAC files, metaflac,
a command-line metadata editor for FLAC files and input plugins for
various music players.

%package     devel
Summary:     Development libraries and header files from FLAC
Requires:    %{name} = %{version}-%{release}

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%package     tools
Summary:     flac and metaflac tools
Requires:    %{name} = %{version}-%{release}

%description tools
This package contains flac and metaflac binaries

%prep
%autosetup -n %{name}-%{version}/%{name}

%build
touch config.rpath
%reconfigure \
    --disable-xmms-plugin \
    --disable-thorough-tests \
    --disable-doxygen-docs \
    --enable-shared \
    --disable-static

%make_build

%install
%make_install

# We don't support man pages on device
rm -rf %{buildroot}/%{_mandir}/

# Test binary segfaults on aarch64
%ifnarch aarch64
%check
make check
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%license COPYING*
%{_libdir}/libFLAC.so.*
%{_libdir}/libFLAC++.so.*

%files devel
%defattr(-, root, root)
%doc AUTHORS README
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_docdir}/%{name}/

%files tools
%defattr(-, root, root,-)
%{_bindir}/flac
%{_bindir}/metaflac
