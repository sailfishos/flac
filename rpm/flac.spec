Summary:       An encoder/decoder for the Free Lossless Audio Codec
Name:          flac
Version:       1.3.1
Release:       0
License:       BSD and GPLv2+
Group:         Applications/Multimedia
Source:        http://downloads.xiph.org/releases/flac/flac-%{version}.tar.gz
URL:           https://xiph.org/flac/
BuildRequires: libogg-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gettext-devel
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
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    pkgconfig

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%package     tools
Summary:     flac and metaflac tools
Group:       Applications/Multimedia
Requires:    %{name} = %{version}-%{release}

%description tools
This package contains flac and metaflac binaries

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
./autogen.sh

%configure \
    --disable-xmms-plugin \
    --disable-thorough-tests \
    --disable-doxygen-docs \
    --enable-shared \
    --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name "*.la" | xargs rm -f

%check
make -C test check

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/*
%{_docdir}/%{name}-*/*

%files tools
%defattr(-, root, root,-)
%{_bindir}/flac
%{_bindir}/metaflac
