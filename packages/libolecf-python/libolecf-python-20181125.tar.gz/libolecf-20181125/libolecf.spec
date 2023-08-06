Name: libolecf
Version: 20181125
Release: 1
Summary: Library to access the Object Linking and Embedding (OLE) Compound File (CF) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libolecf
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
               
BuildRequires: gcc               

%description -n libolecf
Library to access the Object Linking and Embedding (OLE) Compound File (CF) format

%package -n libolecf-devel
Summary: Header files and libraries for developing applications for libolecf
Group: Development/Libraries
Requires: libolecf = %{version}-%{release}

%description -n libolecf-devel
Header files and libraries for developing applications for libolecf.

%package -n libolecf-python2
Obsoletes: libolecf-python < %{version}
Provides: libolecf-python = %{version}
Summary: Python 2 bindings for libolecf
Group: System Environment/Libraries
Requires: libolecf = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libolecf-python2
Python 2 bindings for libolecf

%package -n libolecf-python3
Summary: Python 3 bindings for libolecf
Group: System Environment/Libraries
Requires: libolecf = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libolecf-python3
Python 3 bindings for libolecf

%package -n libolecf-tools
Summary: Several tools for reading Object Linking and Embedding (OLE) Compound Files (CF)
Group: Applications/System
Requires: libolecf = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libolecf-tools
Several tools for reading Object Linking and Embedding (OLE) Compound Files (CF)

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libolecf
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libolecf-devel
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libolecf.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libolecf-python2
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libolecf-python3
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libolecf-tools
%defattr(644,root,root,755)
%license COPYING
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Nov 25 2018 Joachim Metz <joachim.metz@gmail.com> 20181125-1
- Auto-generated

