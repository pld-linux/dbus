#
# Conditional build:
%bcond_without	selinux		# build without SELinux support
%bcond_without	X11		# build without X11 support

%define		expat_version	1:1.95.5
Summary:	D-BUS message bus
Summary(pl.UTF-8):	Magistrala przesyłania komunikatów D-BUS
Name:		dbus
Version:	1.8.4
Release:	1
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
# Source0-md5:	4717cb8ab5b80978fcadf2b4f2f72e1b
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Source4:	%{name}-xinitrc.sh
Source5:	messagebus.upstart
Source6:	%{name}.tmpfiles
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-no_fatal_checks.patch
Patch3:		%{name}-allow-introspection.patch
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	audit-libs-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	doxygen
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	libcap-ng-devel
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.626
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel >= 32
BuildRequires:	xmlto
%{?with_X11:BuildRequires:	xorg-lib-libX11-devel}
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	expat >= %{expat_version}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Provides:	group(messagebus)
Provides:	user(messagebus)
Obsoletes:	dbus-glib-tools
Obsoletes:	dbus-systemd
Conflicts:	pam < 0.99.7.1
# not available for dbus 0.9x yet(?)
#Obsoletes:	dbus-gtk dbus-gcj dbus-gcj-devel dbus-gcj-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%description -l pl.UTF-8
D-BUS to system przesyłania komunikatów pomiędzy aplikacjami. Jest
używany zarówno jako ogólnosystemowa usługa magistrali komunikatów jak
i możliwość przesyłania komunikatów w ramach jednej sesji użytkownika.

%package upstart
Summary:	Upstart job description for system message bus
Summary(pl.UTF-8):	Opis zadania Upstart dla magistrali systemowej DBus
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	upstart >= 0.6

%description upstart
Upstart job description for system message bus.

%description upstart -l pl.UTF-8
Opis zadania Upstart dla magistrali systemowej DBus.

%package libs
Summary:	D-BUS library
Summary(pl.UTF-8):	Biblioteka D-BUS
Group:		Libraries
Obsoletes:	dbus-dirs

%description libs
D-BUS library.

%description libs -l pl.UTF-8
Biblioteka D-BUS.

%package devel
Summary:	Header files for D-BUS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for D-BUS library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki D-BUS.

%package static
Summary:	Static D-BUS library
Summary(pl.UTF-8):	Statyczna biblioteka D-BUS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static D-BUS library.

%description static -l pl.UTF-8
Statyczna biblioteka D-BUS.

%package apidocs
Summary:	D-BUS API documentation
Summary(pl.UTF-8):	Dokumentacja API D-BUS
Group:		Documentation
# dbus.devhelp refers also to common docs packaged in -devel
Requires:	%{name}-devel = %{version}-%{release}

%description apidocs
D-BUS API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API D-BUS.

%package x11
Summary:	X11 session support for D-BUS
Summary(pl.UTF-8):	Obsługa sesji X11 dla D-BUS
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	dbus-X11

%description x11
This package contains D-BUS utilities to start D-BUS service together
with user X11 session.

%description x11 -l pl.UTF-8
Ten pakiet zawiera narzędzia D-BUS pozwalające na uruchomienie usługi
D-BUS wraz z sesją X11 użytkownika.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-verbose-mode} \
	--disable-asserts \
	--disable-silent-rules \
	--disable-tests \
	--enable-abstract-sockets=auto \
	%{?with_selinux:--enable-selinux} \
	--with-console-auth-dir=%{_localstatedir}/run/console/ \
	--with-session-socket-dir=/tmp \
	--with-system-pid-file=%{_localstatedir}/run/dbus.pid \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	%{!?with_X11:--without-x}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{init,profile.d,rc.d/init.d,sysconfig,X11/xinit/xinitrc.d} \
	$RPM_BUILD_ROOT%{_datadir}/dbus-1/{services,interfaces} \
	$RPM_BUILD_ROOT%{_localstatedir}/run/dbus \
	$RPM_BUILD_ROOT%{_localstatedir}/lib/dbus \
	$RPM_BUILD_ROOT/%{_lib} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/messagebus
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d/dbus-daemon-1.sh
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/messagebus
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d
cp -p %{SOURCE5} $RPM_BUILD_ROOT/etc/init/messagebus.conf

install %{SOURCE6} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# upstart (/sbin/init) requires libdbus so it must be in /lib(64)
mv -f $RPM_BUILD_ROOT%{_libdir}/libdbus-1.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libdbus-1.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libdbus-1.so

ln -s dbus.service $RPM_BUILD_ROOT%{systemdunitdir}/messagebus.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 122 messagebus
%useradd -u 122 -d /usr/share/empty -s /bin/false -c "System message bus" -g 122 messagebus

%post
/sbin/chkconfig --add messagebus
%service -n messagebus restart "D-Bus daemon"
export NORESTART="yes"
%systemd_post messagebus.service

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
%systemd_reload

%triggerpostun -- dbus < 1.4.16-5
%systemd_trigger messagebus.service
if [ -f /etc/sysconfig/dbus ]; then
	mv -f /etc/sysconfig/messagebus{,.rpmnew}
	mv -f /etc/sysconfig/{dbus,messagebus}
elif [ -f /etc/sysconfig/dbus.rpmsave ]; then
	mv -f /etc/sysconfig/messagebus{,.rpmnew}
	mv -f /etc/sysconfig/{dbus.rpmsave,messagebus}
fi

%if 0
%post upstart
%upstart_post messagebus

%postun upstart
%upstart_postun messagebus
%endif

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-cleanup-sockets
%attr(755,root,root) %{_bindir}/dbus-daemon
%attr(755,root,root) %{_bindir}/dbus-uuidgen
%attr(755,root,root) %{_bindir}/dbus-monitor
%attr(755,root,root) %{_bindir}/dbus-run-session
%attr(755,root,root) %{_bindir}/dbus-send
%attr(4754,root,messagebus) %{_libdir}/dbus-daemon-launch-helper
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/dbus-1/system-services
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/messagebus
%attr(754,root,root) /etc/rc.d/init.d/messagebus
%attr(755,root,root) /etc/profile.d/dbus-daemon-1.sh
%{systemdtmpfilesdir}/%{name}.conf
%dir %{_localstatedir}/lib/dbus
%dir %{_localstatedir}/run/dbus
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-uuidgen.1*
%{_mandir}/man1/dbus-monitor.1*
%{_mandir}/man1/dbus-run-session.1*
%{_mandir}/man1/dbus-send.1*

%{systemdunitdir}/dbus.service
%{systemdunitdir}/dbus.socket
%{systemdunitdir}/dbus.target.wants/dbus.socket
%{systemdunitdir}/messagebus.service
%{systemdunitdir}/multi-user.target.wants/dbus.service
%{systemdunitdir}/sockets.target.wants/dbus.socket

%if "%{pld_release}" != "ti"
%files upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/messagebus.conf
%endif

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/TODO
%attr(755,root,root) /%{_lib}/libdbus-1.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libdbus-1.so.3
%dir /etc/dbus-1
%dir /etc/dbus-1/system.d
%dir /etc/dbus-1/session.d
%dir %{_datadir}/dbus-1
# interfaces is basically devel thing, but keep dir here
# in case something uses it at runtime
%dir %{_datadir}/dbus-1/interfaces

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-1.so
%{_libdir}/libdbus-1.la
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include
%{_includedir}/dbus-1.0
%{_pkgconfigdir}/dbus-1.pc
%dir %{_docdir}/dbus
%{_docdir}/dbus/*.html
%{_docdir}/dbus/*.png
%{_docdir}/dbus/*.svg
%{_docdir}/dbus/*.txt


%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1.a

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/dbus/api
%{_docdir}/dbus/dbus.devhelp

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-launch
%{_mandir}/man1/dbus-launch.1*
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/dbus-xinitrc.sh
