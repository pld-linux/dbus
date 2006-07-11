#
# TODO:
# - qt4 bindings
#
# Conditional build:
%bcond_without	dotnet	# without .NET support
%bcond_without	gcj	# without Java support
%bcond_without	glib	# without glib support
%bcond_without	gtk	# without GTK+ programs
%bcond_without	python	# without Python support
%bcond_without	qt	# without Qt 3.x support
%bcond_with	qt4	# with Qt 4.x support (broken)
#
%{?with_dotnet:%include	/usr/lib/rpm/macros.mono}

%if %{without glib}
%undefine	with_gtk
%endif

%ifarch i386 alpha sparc sparc64
%undefine with_dotnet
%endif

%define		expat_version	1:1.95.5
%define		glib2_version	1:2.2.0
%define		gtk2_version	2:2.4.0
%define		qt_version	6:3.1.0

Summary:	D-BUS message bus
Summary(pl):	Magistrala przesy�ania komunikat�w D-BUS
Name:		dbus
Version:	0.62
Release:	2
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	ba7692f63d0e9f1ef06703dff56cb650
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-mint.patch
Patch3:		%{name}-python_fixes.patch
Patch4:		%{name}-monodir.patch
Patch5:		%{name}-gcj.patch
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
%{?with_python:BuildRequires:	cpp}
BuildRequires:	doxygen
BuildRequires:	expat-devel >= %{expat_version}
%{?with_gcj:BuildRequires:	gcc-java >= 5:4.0}
%{?with_glib:BuildRequires:	glib2-devel >= %{glib2_version}}
%{?with_gtk:BuildRequires:	gtk+2-devel >= %{gtk2_version}}
BuildRequires:	xorg-lib-libX11-devel
%if %{with dotnet}
BuildRequires:	mono-csharp >= 1.1.7
BuildRequires:	monodoc >= 1.0.7-2
%endif
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-Pyrex >= 0.9.3
BuildRequires:	python-devel >= 2.2
%endif
%{?with_qt:BuildRequires:	qt-devel >= %{qt_version}}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.1
BuildRequires:	QtTest-devel >= 4.1
BuildRequires:	QtXml-devel >= 4.1
BuildRequires:	qt4-build
%endif
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
Provides:	group(messagebus)
Provides:	user(messagebus)
Obsoletes:	dbus-X11
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%description -l pl
D-BUS to system przesy�ania komunikat�w pomi�dzy aplikacjami. Jest
u�ywany zar�wno jako og�lnosystemowa us�uga magistrali komunikat�w jak
i mo�liwo�� przesy�ania komunikat�w w ramach jednej sesji u�ytkownika.

%package devel
Summary:	Header files for D-BUS
Summary(pl):	Pliki nag��wkowe D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for D-BUS.

%description devel -l pl
Pliki nag��wkowe D-BUS.

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
Summary(pl):	Biblioteka do u�ywania D-BUS oparta o GLib
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= %{glib2_version}

%description glib
D-BUS add-on library to integrate the standard D-BUS library with the
GLib thread abstraction and main loop.

%description glib -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcj� w�tk�w i g��wn� p�tl� GLib.

%package glib-devel
Summary:	Header files for GLib-based library for using D-BUS
Summary(pl):	Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}
Requires:	glib2-devel >= %{glib2_version}

%description glib-devel
Header files for GLib-based library for using D-BUS.

%description glib-devel -l pl
Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o GLib.

%package glib-static
Summary:	Static GLib-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u�ywania D-BUS oparta o GLib
Group:		Development/Libraries
Requires:	%{name}-glib-devel = %{version}-%{release}

%description glib-static
Static GLib-based library for using D-BUS.

%description glib-static -l pl
Statyczna biblioteka do u�ywania D-BUS oparta o GLib.

%package glib-tools
Summary:	GLib-based tools for D-BUS
Summary(pl):	Narz�dzia dla D-BUS oparte o GLib
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}

%description glib-tools
GLib-based tools for D-BUS.

%description glib-tools -l pl
Narz�dzia dla D-BUS oparte o GLib

%package gtk
Summary:	GTK+-based graphical D-BUS frontend utility
Summary(pl):	Oparte na GTK+ graficzne narz�dzie do D-BUS
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-X11 = %{version}-%{release}
Requires:	%{name}-glib = %{version}-%{release}

%description gtk
GTK+-based graphical D-BUS frontend utility.

%description gtk -l pl
Oparte na GTK+ graficzne narz�dzie do D-BUS.

%package -n dotnet-%{name}-sharp
Summary:	.NET library for using D-BUS
Summary(pl):	Biblioteka .NET do u�ywania D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mono >= 1.1.7

%description -n dotnet-%{name}-sharp
.NET library for using D-BUS.

%description -n dotnet-%{name}-sharp -l pl
Biblioteka .NET do u�ywania D-BUS.

%package -n dotnet-%{name}-sharp-devel
Summary:	.NET library for using D-BUS with API documentation
Summary(pl):	Biblioteka .NET do u�ywania D-BUS, zawiera dokumentacj� API
Group:		Development/Libraries
Requires:	dotnet-%{name}-sharp = %{version}-%{release}

%description -n dotnet-%{name}-sharp-devel
.NET library for using D-BUS, with API documentation.

%description -n dotnet-%{name}-sharp-devel -l pl
Biblioteka .NET do u�ywania D-BUS, zawiera dokumentacj� API.

%package qt
Summary:	Qt-based library for using D-BUS
Summary(pl):	Biblioteka do u�ywania D-BUS oparta o Qt
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description qt
D-BUS add-on library to integrate the standard D-BUS library with the
Qt thread abstraction and main loop.

%description qt -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z abstrakcj� w�tk�w i g��wn� p�tl� Qt.

%package qt-devel
Summary:	Header files for Qt-based library for using D-BUS
Summary(pl):	Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o Qt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt = %{version}-%{release}

%description qt-devel
Header files for Qt-based library for using D-BUS.

%description qt-devel -l pl
Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o Qt.

%package qt-static
Summary:	Static Qt-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u�ywania D-BUS oparta o Qt
Group:		Development/Libraries
Requires:	%{name}-qt-devel = %{version}-%{release}

%description qt-static
Static Qt-based library for using D-BUS.

%description qt-static -l pl
Statyczna biblioteka do u�ywania D-BUS oparta o Qt.

%package gcj
Summary:	Java library for using D-BUS
Summary(pl):	Biblioteka do u�ywania D-BUS oparta o Jav�
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description gcj
D-BUS add-on library to integrate the standard D-BUS library with
Java.

%description gcj -l pl
Dodatkowa biblioteka D-BUS do integracji standardowej biblioteki D-BUS
z Jav�.

%package gcj-devel
Summary:	Header files for Java-based library for using D-BUS
Summary(pl):	Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o Jav�
Group:		Development/Libraries
Requires:	%{name}-gcj = %{version}-%{release}

%description gcj-devel
Header files for Java-based library for using D-BUS.

%description gcj-devel -l pl
Pliki nag��wkowe biblioteki do u�ywania D-BUS opartej o Jav�.

%package gcj-static
Summary:	Static Java-based library for using D-BUS
Summary(pl):	Statyczna biblioteka do u�ywania D-BUS oparta o Jav�
Group:		Development/Libraries
Requires:	%{name}-gcj-devel = %{version}-%{release}

%description gcj-static
Static Java-based library for using D-BUS.

%description gcj-static -l pl
Statyczna biblioteka do u�ywania D-BUS oparta o Jav�.

%package -n python-dbus
Summary:	Python library for using D-BUS
Summary(pl):	Biblioteka do u�ywania D-BUS oparta o Pythona
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python
Requires:	python-libxml2

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
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i -e 's/DBUS_QT3_LIBS=.*/DBUS_QT3_LIBS="-lqt-mt"/' configure.in

# don't build dotnet-gtk-sharp based examples
# (depends on old gtk-sharp)
sed -i -e 's/example//' mono/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
LDFLAGS="%{rpmldflags} -Wl,--as-needed"
%configure \
	GCJFLAGS="%{rpmcflags}" \
	QTDIR=/usr \
	%{?debug:--enable-verbose-mode} \
	%{?with_dotnet:--enable-mono} \
	%{?with_dotnet:--enable-mono-docs} \
	%{!?with_gcj:--disable-gcj} \
	%{?with_gcj:--enable-gcj} \
	%{!?with_glib:--disable-glib} \
	%{!?with_gtk:--disable-gtk} \
	%{!?with_python:--disable-python} \
	%{?with_qt:--enable-qt3 --with-qt3-moc=/usr/bin/moc} \
	%{?with_qt4:--enable-qt --with-qt-moc=%{_libdir}/qt4/bin/moc}%{!?with_qt4:--with-qt-moc=/NOWHERE} \
	--disable-asserts \
	--disable-tests \
	--enable-abstract-sockets \
	--enable-selinux \
	--with-console-auth-dir=%{_localstatedir}/lock/console/ \
	--with-session-socket-dir=/tmp \
	--with-system-pid-file=%{_localstatedir}/run/dbus.pid \
	--with-xml=expat
%{__make} \
	JAR=fastjar \
	pythondir=%{py_sitedir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/etc/profile.d
install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/dbus

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	JAR=fastjar \
	pythondir=%{py_sitedir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/messagebus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d/dbus-daemon-1.sh
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dbus

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
%service messagebus restart "D-Bus daemon"

%preun
if [ "$1" = "0" ];then
	%service messagebus stop
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
# R: libX11
%attr(755,root,root) %{_bindir}/dbus-launch
%attr(755,root,root) %{_bindir}/dbus-send
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dbus
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) /etc/profile.d/dbus-daemon-1.sh
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/services
%dir %{_localstatedir}/run/dbus
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-launch.1*
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

%if %{with dotnet}
%files -n dotnet-%{name}-sharp
%defattr(644,root,root,755)
%{_prefix}/lib/mono/gac/dbus-sharp

%files -n dotnet-%{name}-sharp-devel
%defattr(644,root,root,755)
%{_prefix}/lib/mono/dbus-sharp
%{_libdir}/monodoc/sources/*
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
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/dbus.pth
%{py_sitedir}/%{name}/*.py[co]
%endif
