#
# TODO: mono
#
# Conditional build:
%bcond_without	glib	# without glib support
%bcond_without	gtk	# without GTK+ programs
%bcond_without	qt	# without qt support
%bcond_without	gcj	# without Java support
%bcond_without	python	# without python support
#
%if %{without glib}
%undefine	with_gtk
%endif
%define expat_version           1.95.5
%define glib2_version           2.2.0
%define qt_version              3.1.0
Summary:	D-BUS message bus
Summary(pl):	Magistrala przesy³ania komunikatów D-BUS
Name:		dbus
Version:	0.21
Release:	1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://www.freedesktop.org/software/%{name}/releases/%{name}-%{version}.tar.gz
# Source0-md5:	311229d60154334ee3f908badc56747d
Source1:	messagebus.init
Patch0:		%{name}-ac.patch
Patch1:		%{name}-nolibs.patch
# NOTE: it's not directory, don't add /
URL:		http://www.freedesktop.org/software/dbus
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	expat-devel >= %{expat_version}
%{?with_glib:BuildRequires:	glib2-devel >= %{glib2_version}}
%{?with_gcj:BuildRequires:	gcc-java-tools}
%{?with_gcj:BuildRequires:	libgcj-devel}
%{?with_gtk:BuildRequires:	gtk+2-devel >= %{glib2_version}}
%{?with_qt:BuildRequires:	kdelibs-devel}
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-devel >= 2.2
Buildrequires:	python-Pyrex >= 0.9-2
%endif
%{?with_qt:BuildRequires:	qt-devel    >= %{qt_version}}
PreReq:	rc-scripts
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):		/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
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
Requires:	%{name} = %{version}-%{release}

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
Requires:	%{name} = %{version}-%{release}

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
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}
Requires:	glib2-devel >= %{glib_version}

%description glib-devel
Header files for GLib-based library for using D-BUS.

%description glib-devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o GLib.

%package glib-static
Summary:	Static GLib-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{version}-%{release}

%description glib-static
Static GLib-based library for using D-BUS.

%description glib-static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o GLib.

%package gtk
Summary:	GTK+-based graphical D-BUS frontend utility
Summary(pl):	Oparte na GTK+ graficzne narzêdzie do D-BUS
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gtk
GTK+-based graphical D-BUS frontend utility.

%description gtk -l pl
Oparte na GTK+ graficzne narzêdzie do D-BUS.

%package qt
Summary:	Qt-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Qt
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

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
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt = %{version}-%{release}
Requires:	kdelibs-devel

%description qt-devel
Header files for Qt-based library for using D-BUS.

%description qt-devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o Qt.

%package qt-static
Summary:	Static Qt-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o Qt
Group:		Development/Libraries
Requires:	%{name}-qt-devel = %{version}-%{release}

%description qt-static
Static Qt-based library for using D-BUS.

%description qt-static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o Qt.

%package gcj
Summary:	Java library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Javê
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description gcj
D-BUS add-on library to integrate the standard D-BUS library with
Java.

%description gcj -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Jav±.

%package gcj-devel
Summary:	Header files for Java-based library for using D-BUS
Summary(pl):	Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o Javê
Group:		Development/Libraries
Requires:	%{name}-gcj = %{version}-%{release}

%description gcj-devel
Header files for Java-based library for using D-BUS.

%description gcj-devel -l pl
Pliki nag³ówkowe biblioteki do u¿ywania D-BUS opartej o Javê.

%package gcj-static
Summary:	Static Java-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u¿ywania D-BUS oparta o Javê
Group:		Development/Libraries
Requires:	%{name}-gcj-devel = %{version}-%{release}

%description gcj-static
Static Java-based library for using D-BUS.

%description gcj-static -l pl
Statyczna biblioteka do u¿ywania D-BUS oparta o Javê.

%package -n python-dbus
Summary:	Python library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Pythona
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-dbus
D-BUS add-on library to integrate the standard D-BUS library with
Python.

%description -n python-dbus -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Pythonem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	QTDIR=/usr \
	%{!?with_glib:--disable-glib} \
	%{!?with_gtk:--disable-gtk} \
	%{!?with_qt:--disable-qt} \
	%{!?with_python:--disable-python} \
	%{!?with_gcj:--disable-gcj} \
	%{?with_gcj:--enable-gcj} \
	--disable-tests \
	--disable-verbose-mode \
	--disable-asserts

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/messagebus

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid messagebus`" ]; then
	if [ "`getgid messagebus`" != "122" ]; then
		echo "Error: group messagebus doesn't have gid=122. Correct this before installing dbus." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 122 -r -f messagebus
fi
if [ -n "`/bin/id -u messagebus 2>/dev/null`" ]; then
	if [ "`/bin/id -u messagebus`" != "122" ]; then
		echo "Error: user messagebus doesn't have uid=122. Correct this before installing dbus." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 122 -r -d /usr/share/empty -s /bin/false -c "System message bus" -g messagebus messagebus 1>&2
fi

%post
/sbin/ldconfig
/sbin/chkconfig --add messagebus
if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart >&2
else
	echo "Run \"/etc/rc.d/init.d/messagebus start\" to start D-Bus daemon."
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/messagebus ]; then
		/etc/rc.d/init.d/messagebus stop >&2
	fi
	/sbin/chkconfig --del messagebus
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	/usr/sbin/userdel messagebus
	/usr/sbin/groupdel messagebus
fi
		
%post   glib -p /sbin/ldconfig
%postun glib -p /sbin/ldconfig

%post   qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

%post   gcj -p /sbin/ldconfig
%postun gcj -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_bindir}/dbus-cleanup-sockets
%attr(755,root,root) %{_bindir}/dbus-daemon-1
# dbus-launch R: XFree86-libs
%attr(755,root,root) %{_bindir}/dbus-launch
%attr(755,root,root) %{_bindir}/dbus-send
%attr(755,root,root) %{_libdir}/libdbus-1.so.*.*.*
%dir %{_libdir}/dbus-*
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/dbus-1/*.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_localstatedir}/run/dbus
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon-1.1*
%{_mandir}/man1/dbus-launch.1*
%{_mandir}/man1/dbus-send.1*
#%{_libdir}/dbus-1.0/services

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,txt}
%attr(755,root,root) %{_libdir}/libdbus-1.so
%{_libdir}/libdbus-1.la
%{_libdir}/dbus-*/include
%{_pkgconfigdir}/dbus-1.pc
%{_includedir}/dbus*
%{?with_glib:%exclude %{_includedir}/dbus*/dbus/dbus-glib.h}
%{?with_qt:%exclude %{_includedir}/dbus*/dbus/dbus-qt.h}

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1.a

%if %{with glib}
%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-glib-tool
%attr(755,root,root) %{_bindir}/dbus-monitor
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so.*.*.*
%{_mandir}/man1/dbus-monitor.1*

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so
%{_libdir}/libdbus-glib-1.la
%{_includedir}/dbus*/dbus/dbus-glib.h
%{_pkgconfigdir}/dbus-glib-1.pc

%files glib-static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib-1.a
%endif

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-viewer
%endif

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-qt-1.so.*.*.*

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-qt-1.so
%{_libdir}/libdbus-qt-1.la
%{_includedir}/dbus*/dbus/dbus-qt.h

%files qt-static
%defattr(644,root,root,755)
%{_libdir}/libdbus-qt-1.a
%endif

%if %{with gcj}
%files gcj
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*gcj*.so.*.*.*

%files gcj-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*gcj*.so
%{_libdir}/lib*gcj*.la
%{_datadir}/java/*.jar

%files gcj-static
%defattr(644,root,root,755)
%{_libdir}/lib*gcj*.a
%endif

%if %{with python}
%files -n python-dbus
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py[co]
%endif
