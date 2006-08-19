#
%define		expat_version	1:1.95.5
#
Summary:	D-BUS message bus
Summary(pl):	Magistrala przesy³ania komunikatów D-BUS
Name:		dbus
Version:	0.92
Release:	2
License:	AFL v2.1 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	ea2be58c80a80631ba5b3c92cffd335c
Source1:	messagebus.init
Source2:	%{name}-daemon-1-profile.d-sh
Source3:	%{name}-sysconfig
Source4:	%{name}-xinitrc.sh
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-config.patch
URL:		http://www.freedesktop.org/Software/dbus
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	expat-devel >= %{expat_version}
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
Requires:	rc-scripts
Provides:	group(messagebus)
Provides:	user(messagebus)
Obsoletes:	dbus-X11
Obsoletes:	dbus-glib-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%description -l pl
D-BUS to system przesy³ania komunikatów pomiêdzy aplikacjami. Jest
u¿ywany zarówno jako ogólnosystemowa us³uga magistrali komunikatów jak
i mo¿liwo¶æ przesy³ania komunikatów w ramach jednej sesji u¿ytkownika.

%package libs
Summary:	D-BUS libraries
Summary(pl):	Biblioteki D-BUS
Group:		Libraries

%description libs
D-BUS libraries.

%description libs -l pl
Biblioteki D-BUS.

%package devel
Summary:	Header files for D-BUS
Summary(pl):	Pliki nag³ówkowe D-BUS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for D-BUS.

%description devel -l pl
Pliki nag³ówkowe D-BUS.

%package static
Summary:	Static D-BUS libraries
Summary(pl):	Statyczne biblioteki D-BUS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static D-BUS libraries.

%description static -l pl
Statyczne biblioteki D-BUS.

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
	%{?debug:--enable-verbose-mode} \
	--disable-asserts \
	--disable-tests \
	--enable-abstract-sockets \
	--enable-selinux \
	--with-console-auth-dir=%{_localstatedir}/lock/console/ \
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
install -d $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
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

%triggerpostun -- %{name} < 0.92
%banner %{name} << EOF
WARNING!!!
configuration file /etc/sysconfig/dbus has been moved to /etc/sysconfig/messagebus!
EOF

if [ -f /etc/sysconfig/dbus ]; then
    mv /etc/sysconfig/dbus /etc/sysconfig/messagebus
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbus-cleanup-sockets
%attr(755,root,root) %{_bindir}/dbus-daemon
# R: libX11
%attr(755,root,root) %{_bindir}/dbus-launch
%attr(755,root,root) %{_bindir}/dbus-monitor
%attr(755,root,root) %{_bindir}/dbus-send
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/*.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/messagebus
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) /etc/profile.d/dbus-daemon-1.sh
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh

%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/services
%dir %{_localstatedir}/run/dbus
%{_mandir}/man1/dbus-cleanup-sockets.1*
%{_mandir}/man1/dbus-daemon.1*
%{_mandir}/man1/dbus-launch.1*
%{_mandir}/man1/dbus-monitor.1*
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

%files static
%defattr(644,root,root,755)
%{_libdir}/libdbus-1.a
