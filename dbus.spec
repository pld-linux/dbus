%define		expat_version	1:1.95.5
Summary:	D-BUS message bus
Summary(pl.UTF-8):	Magistrala przesyłania komunikatów D-BUS
Name:		dbus
Version:	1.1.4
Release:	3
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
# Source0-md5:	e08fdf702cae648acd9780eca0ce4df6
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Source4:	%{name}-xinitrc.sh
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-no_fatal_checks.patch
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	audit-libs-devel
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	expat-devel >= %{expat_version}
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	expat >= %{expat_version}
Requires:	rc-scripts
Provides:	group(messagebus)
Provides:	user(messagebus)
Conflicts:	pam < 0.99.7.1
Obsoletes:	dbus-X11
Obsoletes:	dbus-glib-tools
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
Summary:	D-BUS libraries
Summary(pl.UTF-8):	Biblioteki D-BUS
Group:		Libraries

%description libs
D-BUS libraries.

%description libs -l pl.UTF-8
Biblioteki D-BUS.

%package devel
Summary:	Header files for D-BUS
Summary(pl.UTF-8):	Pliki nagłówkowe D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for D-BUS.

%description devel -l pl.UTF-8
Pliki nagłówkowe D-BUS.

%package static
Summary:	Static D-BUS libraries
Summary(pl.UTF-8):	Statyczne biblioteki D-BUS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static D-BUS libraries.

%description static -l pl.UTF-8
Statyczne biblioteki D-BUS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-verbose-mode} \
	--disable-asserts \
	--disable-tests \
	--enable-abstract-sockets \
	--enable-selinux \
	--with-console-auth-dir=%{_localstatedir}/run/console/ \
	--with-session-socket-dir=/tmp \
	--with-system-pid-file=%{_localstatedir}/run/dbus.pid \
	--with-xml=expat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/profile.d
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/etc/sysconfig
install -d $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d
install -d $RPM_BUILD_ROOT%{_datadir}/dbus-1/{services,interfaces}
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/dbus

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/messagebus
install %{SOURCE2} $RPM_BUILD_ROOT/etc/profile.d/dbus-daemon-1.sh
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/messagebus
install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 122 messagebus
%useradd -u 122 -d /usr/share/empty -s /bin/false -c "System message bus" -g 122 messagebus

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

%triggerpostun -- %{name} < 0.92
%banner %{name} << EOF
WARNING!!!
configuration file /etc/sysconfig/dbus has been moved to /etc/sysconfig/messagebus!
EOF

if [ -f /etc/sysconfig/dbus ]; then
	mv -f /etc/sysconfig/messagebus{,.rpmnew}
	mv -f /etc/sysconfig/{dbus,messagebus}
elif [ -f /etc/sysconfig/dbus.rpmsave ]; then
	mv -f /etc/sysconfig/messagebus{,.rpmnew}
	mv -f /etc/sysconfig/{dbus.rpmsave,messagebus}
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-cleanup-sockets
%attr(755,root,root) %{_bindir}/dbus-daemon
%attr(755,root,root) %{_bindir}/dbus-uuidgen
# R: libX11
%attr(755,root,root) %{_bindir}/dbus-launch
%attr(755,root,root) %{_bindir}/dbus-monitor
%attr(755,root,root) %{_bindir}/dbus-send
%attr(4754,root,messagebus) %{_libdir}/dbus-daemon-launch-helper
%dir %{_libdir}/dbus-1
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/interfaces
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/dbus-1/system-services
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/*.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_sysconfdir}/dbus-1/session.d
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/messagebus
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) /etc/profile.d/dbus-daemon-1.sh
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%dir %{_localstatedir}/run/dbus
%dir /var/lib/dbus
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-uuidgen.1*
%{_mandir}/man1/dbus-launch.1*
%{_mandir}/man1/dbus-monitor.1*
%{_mandir}/man1/dbus-send.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/TODO
%attr(755,root,root) %{_libdir}/libdbus-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdbus-1.so.3

%files devel
%defattr(644,root,root,755)
%doc doc/*.{html,txt}
%attr(755,root,root) %{_libdir}/libdbus-1.so
%{_libdir}/libdbus-1.la
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include
%{_pkgconfigdir}/dbus-1.pc
%{_includedir}/dbus-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1.a
