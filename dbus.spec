%define gettext_package dbus
%define expat_version           1.95.5
%define glib2_version           2.2.0
%define qt_version              3.1.0

Summary:	D-BUS message bus
Name:		dbus
Version:	0.11
Release:	1
Source0:	http://www.freedesktop.org/software/dbus/releases/%{name}-%{version}.tar.gz
# Source0-md5:	87f8cf7ffd114846d577e454ef3129aa
Patch0:		%{name}-ac.patch
URL:		http://www.freedesktop.org/software/dbus/
License:	AFL/GPL
Group:		Libraries
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
PreReq:		chkconfig
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	qt-devel    >= %{qt_version}
BuildRequires:	kdelibs-devel

%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%package devel
Summary:	Libraries and headers for D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Headers and static libraries for D-BUS.

%package glib
Summary:	GLib-based library for using D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description glib
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.


%package qt
Summary:	Qt-based library for using D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description qt
D-BUS add-on library to integrate the standard D-BUS library with the
Qt thread abstraction and main loop.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
COMMON_ARGS="--enable-glib=yes --enable-qt=yes"
export QTDIR=/usr

%configure $COMMON_ARGS \
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
rm -rf %{buildroot}

%pre
# Add the "messagebus" user
#/usr/sbin/useradd -c 'System message bus' -u 81 \
#	-s /sbin/nologin -r -d '/' messagebus 2> /dev/null || :

%post
/sbin/ldconfig
#/sbin/chkconfig --add messagebus

%preun
#if [ $1 = 0 ]; then
#    service messagebus stop > /dev/null 2>&1
#    /sbin/chkconfig --del messagebus
#fi

%postun
/sbin/ldconfig
#if [ "$1" -ge "1" ]; then
#  service messagebus condrestart > /dev/null 2>&1
#fi

%post   glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post   qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

##  -f %{gettext_package}.lang
%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/dbus-1/*.conf
#/etc/rc.d/init.d/*
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_localstatedir}/run/dbus
%dir %{_libdir}/dbus-*
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*dbus-1*.so.*
%{_mandir}/man*/*
#%{_libdir}/dbus-1.0/services

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdbus-1*.so
%{_libdir}/libdbus-1*.la
%{_libdir}/dbus-*/include
%{_pkgconfigdir}/*
%{_includedir}/*
%{_libdir}/lib*.a

%files glib
%defattr(644,root,root,755)
%{_libdir}/*glib*.so.*.*

%files qt
%defattr(644,root,root,755)
%{_libdir}/*qt*.so.*.*
