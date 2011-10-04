Summary: An encoder/decoder for the Free Lossless Audio Codec
Name: flac
Version: 1.2.1
Release: 4
License: BSD and GPLv2+
Group: Applications/Multimedia
Source: http://prdownloads.sourceforge.net/flac/flac-%{version}.tar.gz
Patch1: flac-1.2.1-asm.patch
Patch2: flac-1.2.1-gcc43.patch
Patch3: flac-1.2.1-hidesyms.patch
Patch4: flac-1.2.1-tests.patch
Patch5: flac-1.2.1-cflags.patch
Patch6: flac-1.2.1-bitreader.patch
URL: http://flac.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libogg-devel
BuildRequires: automake autoconf libtool gettext-devel
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

%package devel
Summary: Development libraries and header files from FLAC
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%prep
%setup -q
%patch1 -p1 -b .asm
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .hidesyms
# reduce number of tests
%patch4 -p1 -b .tests
%patch5 -p1 -b .cflags
%patch6 -p0 -b .bitreader

%build
./autogen.sh -V

%configure \
    --disable-xmms-plugin \
    --disable-thorough-tests

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find doc/ -name "Makefile*" -exec rm -f {} \;

%check
make -C test check &> /dev/null

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%doc AUTHORS COPYING* README
%{_bindir}/flac
%{_bindir}/metaflac
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%doc doc/html
%{_includedir}/*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*.m4
