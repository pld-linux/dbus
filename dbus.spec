#
# Conditional build:
%bcond_without	glib	# without glib support
%bcond_without	gtk	# without GTK+ programs
%bcond_without	qt	# without Qt support
%bcond_without	python	# without Python support
%bcond_without	dotnet	# without .NET support
%bcond_with	gcj	# with Java support
#
%if %{without glib}
%undefine	with_gtk
%endif

%define		expat_version	1.95.5
%define		glib2_version	2.2.0
%define		qt_version	3.1.0
Summary:	D-BUS message bus
Summary(pl):	Magistrala przesy³ania komunikatów D-BUS
Name:		dbus
Version:	0.36.2
Release:	2
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	45468e46967d3e70f082d0d0e6049225
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Source4:	%{name}-xinitrc.sh
Patch0:		%{name}-ac.patch
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}-config.patch
Patch3:		%{name}-mint.patch
Patch4:		%{name}-python_fixes.patch
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	doxygen
%{?with_glib:BuildRequires:	glib2-devel >= %{glib2_version}}
%{?with_gcj:BuildRequires:	gcc-java >= 5:4.0}
%{?with_gtk:BuildRequires:	gtk+2-devel >= %{glib2_version}}
%{?with_qt:BuildRequires:	kdelibs-devel}
# just gtk-sharp for examples
%{?with_dotnet:BuildRequires:	dotnet-gtk-sharp-devel}
%{?with_dotnet:BuildRequires:	mono-csharp >= 0.95}
%{?with_dotnet:BuildRequires:	monodoc >= 1.0.7-2}
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-Pyrex >= 0.9.3
%endif
%{?with_qt:BuildRequires:	qt-devel >= %{qt_version}}
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
Requires:	rc-scripts
Requires:	%{name}-libs = %{version}-%{release}
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(messagebus)
Provides:	user(messagebus)
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
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for D-BUS.

%description devel -l pl
Pliki nag³ówkowe D-BUS.

%package libs
Summary:	D-BUS libraries
Summary(pl):	Biblioteki D-BUS
Group:		Libraries

%description libs
D-BUS libraries.

%description libs -l pl
Biblioteki D-BUS.

%package static
Summary:	Static D-BUS libraries
Summary(pl):	Statyczne biblioteki D-BUS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static D-BUS libraries.

%description static -l pl
Statyczne biblioteki D-BUS.

%package glib
Summary:	GLib-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o GLib
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= %{glib2_version}

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
Requires:	glib2-devel >= %{glib2_version}

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

%package glib-tools
Summary:	GLib-based tools for D-BUS
Summary(pl):	Narzêdzia dla D-BUS oparte o GLib
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}

%description glib-tools
GLib-based tools for D-BUS.

%description glib-tools -l pl
Narzêdzia dla D-BUS oparte o GLib

%package gtk
Summary:	GTK+-based graphical D-BUS frontend utility
Summary(pl):	Oparte na GTK+ graficzne narzêdzie do D-BUS
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}

%description gtk
GTK+-based graphical D-BUS frontend utility.

%description gtk -l pl
Oparte na GTK+ graficzne narzêdzie do D-BUS.

%package X11
Summary:	X11 D-BUS utilities
Summary(pl):	Narzêdzia X11 D-BUSa
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	xinitrc

%description X11
X11 D-BUS utilities.

%description X11 -l pl
Narzêdzia X11 D-BUSa.

%package -n dotnet-%{name}-sharp
Summary:	.NET library for using D-BUS
Summary(pl):	Biblioteka .NET do u¿ywania D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	mono

%description -n dotnet-%{name}-sharp
.NET library for using D-BUS.

%description -n dotnet-%{name}-sharp -l pl
Biblioteka .NET do u¿ywania D-BUS.

%package -n dotnet-%{name}-sharp-devel
Summary:	.NET library for using D-BUS with API documentation
Summary(pl):	Biblioteka .NET do u¿ywania D-BUS, zawiera dokumentacjê API
Group:		Development/Libraries
Requires:	dotnet-%{name}-sharp = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description -n dotnet-%{name}-sharp-devel
.NET library for using D-BUS, with API documentation.

%description -n dotnet-%{name}-sharp-devel -l pl
Biblioteka .NET do u¿ywania D-BUS, zawiera dokumentacjê API.

%package qt
Summary:	Qt-based library for using D-BUS
Summary(pl):	Biblioteka do u¿ywania D-BUS oparta o Qt
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

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
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python

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
%patch2 -p1
%patch3 -p0
%patch4 -p1
sed -i 's:JAR.*=.*jar:JAR=fastjar:g' gcj/Makefile.{am,in}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	QTDIR=/usr \
	%{?debug:--enable-verbose-mode} \
	%{!?with_dotnet:--disable-mono} \
	%{!?with_dotnet:--disable-mono-docs} \
	%{!?with_gcj:--disable-gcj} \
	%{?with_gcj:--enable-gcj} \
	%{!?with_glib:--disable-glib} \
	%{!?with_gtk:--disable-gtk} \
	%{!?with_python:--disable-python} \
	%{!?with_qt:--disable-qt} \
	--disable-asserts \
	--disable-tests \
	--enable-abstract-sockets \
	--enable-selinux \
	--enable-verbose-mode \
	--with-session-socket-dir=/tmp \
	--with-system-pid-file=%{_localstatedir}/run/dbus.pid \
	--with-system-socket=%{_localstatedir}/lib/dbus-1/system_bus_socket
	--with-xml=expat
%{__make} \
	pythondir=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/etc/profile.d
install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
install -d $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/dbus-1
%if %{with dotnet}
install -d $RPM_BUILD_ROOT%{_libdir}/monodoc/sources
%endif

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pythondir=%{py_sitedir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/messagebus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d/dbus-daemon-1.sh
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dbus
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/dbus.sh

%if %{with python}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{name}/*.{py,la,a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 122 messagebus
%useradd -u 122 -d /usr/share/empty -s /bin/false -c "System message bus" -g messagebus messagebus

%post
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
if [ "$1" = "0" ]; then
	%userremove messagebus
	%groupremove messagebus
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%post	gcj -p /sbin/ldconfig
%postun	gcj -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-cleanup-sockets
%attr(755,root,root) %{_bindir}/dbus-daemon
%attr(755,root,root) %{_bindir}/dbus-send
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dbus
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) /etc/profile.d/dbus-daemon-1.sh
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/services
%dir %{_localstatedir}/lib/dbus-1
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-send.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_libdir}/libdbus-1.so.*.*.*
%dir %{_libdir}/dbus-*

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,txt}
%attr(755,root,root) %{_libdir}/libdbus-1.so
%{_libdir}/libdbus-1.la
%{_libdir}/dbus-*/include
%{_pkgconfigdir}/dbus-1.pc
%{_includedir}/dbus*
%{?with_glib:%exclude %{_includedir}/dbus*/dbus/dbus-glib*.h}
%{?with_qt:%exclude %{_includedir}/dbus*/dbus/dbus-qt.h}

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1.a

%if %{with glib}
%files glib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so.*.*.*

%files glib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-binding-tool
%attr(755,root,root) %{_libdir}/libdbus-glib-1.so
%{_libdir}/libdbus-glib-1.la
%{_includedir}/dbus*/dbus/dbus-glib*.h
%{_pkgconfigdir}/dbus-glib-1.pc

%files glib-static
%defattr(644,root,root,755)
%{_libdir}/libdbus-glib-1.a

%files glib-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-monitor
%{_mandir}/man1/dbus-monitor.1*
%endif

%if %{with gtk}
%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-viewer
%endif

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-launch
%attr(755,root,root) %{_sysconfdir}/X11/xinit/xinitrc.d/dbus.sh
%{_mandir}/man1/dbus-launch.1*

%if %{with dotnet}
%files -n dotnet-%{name}-sharp
%defattr(644,root,root,755)
%dir %{_libdir}/mono/gac/dbus-sharp
%{_libdir}/mono/gac/dbus-sharp/*

%files -n dotnet-%{name}-sharp-devel
%defattr(644,root,root,755)
%{_libdir}/monodoc/sources/*
%dir %{_libdir}/mono/dbus-sharp
%{_libdir}/mono/dbus-sharp/*
%{_pkgconfigdir}/dbus-sharp.pc
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
%dir %{py_sitedir}/%{name}/
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/dbus.pth
%{py_sitedir}/%{name}/*.py[co]
%endif
