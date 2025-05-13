# TODO:
# - enable ducktype-docs when it works and update files if necessary
# - move /etc/dbus-1 from -libs to base after external packages transition to /usr/share/dbus-1
#
# Conditional build:
%bcond_without	apidocs		# API docs
%bcond_without	apparmor	# AppArmor support
%bcond_with	ducktype	# ducktype docs
%bcond_without	selinux		# SELinux support
%bcond_without	systemd		# systemd at_console support
%bcond_without	X11		# X11 support

%define		expat_version	1:1.95.5
Summary:	D-BUS message bus
Summary(pl.UTF-8):	Magistrala przesyłania komunikatów D-BUS
Name:		dbus
Version:	1.14.10
Release:	2
License:	AFL v2.1 or GPL v2+
Group:		Libraries
Source0:	https://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.xz
# Source0-md5:	46070a3487817ff690981f8cd2ba9376
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Source4:	%{name}-xinitrc.sh
Source5:	%{name}.tmpfiles
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-no_fatal_checks.patch
Patch3:		%{name}-allow-introspection.patch
Patch4:		%{name}-autoconf-archive.patch
Patch5:		log-commands.patch
URL:		https://www.freedesktop.org/Software/dbus
BuildRequires:	audit-libs-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	autoconf-archive >= 2019.01.06
BuildRequires:	automake >= 1:1.13
BuildRequires:	docbook-dtd44-xml
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= %{expat_version}
%{?with_apparmor:BuildRequires:	libapparmor-devel >= 1:2.10}
BuildRequires:	libcap-ng-devel
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.0.86}
BuildRequires:	libtool >= 2:2.0
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
%{?with_ducktype:BuildRequires:	python3-ducktype}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.011
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 32}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
%{?with_X11:BuildRequires:	xorg-lib-libX11-devel}
BuildRequires:	xz
%{?with_ducktype:BuildRequires:	yelp-tools}
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun,postun):	systemd-units >= 1:250.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	expat >= %{expat_version}
%{?with_apparmor:Requires:	libapparmor >= 1:2.10}
%{?with_selinux:Requires:	libselinux >= 2.0.86}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 1:250.1
Provides:	group(messagebus)
Provides:	user(messagebus)
Obsoletes:	dbus-glib-tools < 0.91
Obsoletes:	dbus-systemd < 1.4.16-5
Obsoletes:	dbus-upstart < 1.8.16-3
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

%package libs
Summary:	D-BUS library
Summary(pl.UTF-8):	Biblioteka D-BUS
Group:		Libraries
%{?with_systemd:Requires:	systemd-libs >= 32}
Obsoletes:	dbus-dirs < 1.6.14

%description libs
D-BUS library.

%description libs -l pl.UTF-8
Biblioteka D-BUS.

%package devel
Summary:	Header files for D-BUS library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_systemd:Requires:	systemd-devel >= 32}

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
BuildArch:	noarch

%description apidocs
D-BUS API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API D-BUS.

%package x11
Summary:	X11 session support for D-BUS
Summary(pl.UTF-8):	Obsługa sesji X11 dla D-BUS
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	dbus-X11 < 0.62-2

%description x11
This package contains D-BUS utilities to start D-BUS service together
with user X11 session.

%description x11 -l pl.UTF-8
Ten pakiet zawiera narzędzia D-BUS pozwalające na uruchomienie usługi
D-BUS wraz z sesją X11 użytkownika.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' tools/GetAllMatchRules.py

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-doxygen-docs} \
	%{!?with_apparmor:--disable-apparmor} \
	--disable-asserts \
	%{!?with_ducktype:--disable-ducktype-docs} \
	%{?debug:--enable-verbose-mode} \
	%{!?with_selinux:--disable-selinux} \
	--disable-silent-rules \
	%{!?with_systemd:--disable-systemd} \
	--disable-tests \
	--enable-user-session \
	--with-console-auth-dir=%{_localstatedir}/run/console/ \
	--with-session-socket-dir=/tmp \
	--with-system-pid-file=%{_localstatedir}/run/dbus.pid \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	%{!?with_X11:--without-x}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{profile.d,rc.d/init.d,sysconfig,X11/xinit/xinitrc.d} \
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

cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%if %{with systemd}
ln -s dbus.service $RPM_BUILD_ROOT%{systemdunitdir}/messagebus.service

# we are creating messagebus user from rpm pre
%{__rm} $RPM_BUILD_ROOT/usr/lib/sysusers.d/dbus.conf
%endif

# for local configuration in dbus 1.10+
install -d $RPM_BUILD_ROOT/etc/dbus-1/{session.d,system.d}

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
%systemd_user_post dbus.service dbus.socket

%preun
if [ "$1" = "0" ];then
	%service messagebus stop
	/sbin/chkconfig --del messagebus
fi
%systemd_user_preun dbus.service dbus.socket

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
%attr(755,root,root) %{_bindir}/dbus-test-tool
%attr(755,root,root) %{_bindir}/dbus-update-activation-environment
%attr(4754,root,messagebus) %{_libexecdir}/dbus-daemon-launch-helper
%{_datadir}/dbus-1/session.conf
%{_datadir}/dbus-1/system.conf
%{_datadir}/xml/dbus-1
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/session.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.conf
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
%{_mandir}/man1/dbus-test-tool.1*
%{_mandir}/man1/dbus-update-activation-environment.1*

%if %{with systemd}
%{systemdunitdir}/dbus.service
%{systemdunitdir}/dbus.socket
%{systemdunitdir}/messagebus.service
%{systemdunitdir}/multi-user.target.wants/dbus.service
%{systemdunitdir}/sockets.target.wants/dbus.socket
%{systemduserunitdir}/dbus.service
%{systemduserunitdir}/dbus.socket
%{systemduserunitdir}/sockets.target.wants/dbus.socket
%endif

%files libs
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md COPYING NEWS README doc/TODO
%attr(755,root,root) %{_libdir}/libdbus-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbus-1.so.3
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/session.d
%dir %{_datadir}/dbus-1/system.d
# interfaces is basically devel thing, but keep dir here
# in case something uses it at runtime
%dir %{_datadir}/dbus-1/interfaces
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/dbus-1/system-services
# TODO: now it's only for local configuration - move to base dbus package
#       after all packages place constant configuration in %{_datadir}/dbus-1
%dir /etc/dbus-1
%dir /etc/dbus-1/session.d
%dir /etc/dbus-1/system.d

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdbus-1.so
%{_libdir}/libdbus-1.la
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include
%{_libdir}/cmake/DBus1
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

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/dbus/api
%{_docdir}/dbus/dbus.devhelp2
%endif

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-launch
%{_mandir}/man1/dbus-launch.1*
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/dbus-xinitrc.sh
