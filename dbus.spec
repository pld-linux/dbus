#
# Conditional build:
# _without_glib - without glib support
# _without_qt - without qt support
#
%define gettext_package dbus
%define expat_version           1.95.5
%define glib2_version           2.2.0
%define qt_version              3.1.0
Summary:	D-BUS message bus
Summary(pl):	Magistrala przesy³ania komunikatów D-BUS
Name:		dbus
Version:	0.13
Release:	1
License:	AFL/GPL
Group:		Libraries
Source0:	http://www.freedesktop.org/software/%{name}/releases/%{name}-%{version}.tar.gz
# Source0-md5:	b7f29a4b581445a1290df84d1fbb31ee
Patch0:		%{name}-ac.patch
Patch1:		%{name}-nolibs.patch
URL:		http://www.freedesktop.org/software/dbus/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	expat-devel >= %{expat_version}
%{!?_without_glib:BuildRequires:	glib2-devel >= %{glib2_version}}
%{!?_without_qt:BuildRequires:	kdelibs-devel}
BuildRequires:	libtool
%{!?_without_qt:BuildRequires:	qt-devel    >= %{qt_version}}
#PreReq:	rc-scripts
#Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%description -l pl
D-BUS to system przesy³ania komunikatów pomiêdzy aplikacjami. Jest
u¿ywany zarówno jako ogólnosystemowa us³uga magistrali komunikatów jak
i mo¿liwo¶æ przesy³ania komunikatów w ramach jednej sesji u¿ytkownika.

%package devel
Summary:	Header files for D-BUS
Summary(pl):	Pliki nag³ówkowe D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for D-BUS.

%description devel -l pl
Pliki nag³ówkowe D-BUS.

%package static
Summary:	Static D-BUS libraries
Summary(pl):	Statyczne biblioteki D-BUS
Group:		Development/Libraries

%description static
Static D-BUS libraries.

%description static -l pl
Statyczne biblioteki D-BUS.

%package glib
Summary:	GLib-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o GLib
Group:		Libraries
Requires:	%{name} = %{version}

%description glib
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.

%description glib -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcj± w±tków i g³ówn± pêtl± GLib.

%package glib-devel
Summary:	Header files for GLib-based library for using D-BUS
Summary(pl):	Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Requires:	%{name}-glib = %{version}

%description glib-devel
Header files for GLib-based library for using D-BUS.

%description glib-devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o GLib.

%package glib-static
Summary:	Static GLib-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{version}

%description glib-static
Static GLib-based library for using D-BUS.

%description glib-static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o GLib.

%package qt
Summary:	Qt-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Qt
Group:		Libraries
Requires:	%{name} = %{version}

%description qt
D-BUS add-on library to integrate the standard D-BUS library with the
Qt thread abstraction and main loop.

%description qt -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcj± w±tków i g³ówn± pêtl± Qt.

%package qt-devel
Summary:	Header files for Qt-based library for using D-BUS
Summary(pl):	Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o Qt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Requires:	%{name}-qt = %{version}

%description qt-devel
Header files for Qt-based library for using D-BUS.

%description qt-devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o Qt.

%package qt-static
Summary:	Static Qt-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o Qt
Group:		Development/Libraries
Requires:	%{name}-qt-devel = %{version}

%description qt-static
Static Qt-based library for using D-BUS.

%description qt-static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o Qt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	QTDIR=/usr \
	%{?_without_glib:--disable-glib} \
	%{?_without_qt:--disable-qt} \
	--disable-tests \
	--disable-verbose-mode \
	--disable-asserts
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

## %find_lang %{gettext_package}

%clean
rm -rf $RPM_BUILD_ROOT

#%pre
# Add the "messagebus" user
#/usr/sbin/useradd -c 'System message bus' -u 81 \
#	-s /sbin/nologin -r -d '/' messagebus 2> /dev/null || :

%post	-p /sbin/ldconfig
#/sbin/chkconfig --add messagebus

#%preun
#if [ $1 = 0 ]; then
#    service messagebus stop > /dev/null 2>&1
#    /sbin/chkconfig --del messagebus
#fi

%postun	-p /sbin/ldconfig

%post   glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post   qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

##  -f %{gettext_package}.lang
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libdbus-1*.so.*.*.*
%dir %{_libdir}/dbus-*
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/dbus-1/*.conf
#/etc/rc.d/init.d/*
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_localstatedir}/run/dbus
%{_mandir}/man*/*
#%{_libdir}/dbus-1.0/services

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,txt} HACKING
%attr(755,root,root) %{_libdir}/libdbus-1*.so
%{_libdir}/libdbus-1*.la
%{_libdir}/dbus-*/include
%{_pkgconfigdir}/dbus-1.pc
%{_includedir}/dbus*
%{!?_without_glib:%exclude %{_includedir}/dbus*/dbus/dbus-glib.h}
%{!?_without_qt:%exclude %{_includedir}/dbus*/dbus/dbus-qt.h}

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1*.a

%if 0%{!?_without_glib:1}
%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-glib*.so.*.*
%{_pkgconfigdir}/dbus-glib-1.pc

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-glib*.so
%{_libdir}/libdbus-glib*.la
%{_includedir}/dbus*/dbus/dbus-glib.h

%files glib-static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib*.a
%endif

%if 0%{!?_without_qt:1}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-qt*.so.*.*

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-qt*.so
%{_libdir}/libdbus-qt*.la
%{_includedir}/dbus*/dbus/dbus-qt.h

%files qt-static
%defattr(644,root,root,755)
%{_libdir}/libdbus-qt*.a
%endif
