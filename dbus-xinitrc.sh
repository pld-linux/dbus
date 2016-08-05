#! /bin/sh

[ -x /usr/bin/dbus-launch -a -f /var/run/dbus.pid ] || return

# Get configuration
. /etc/sysconfig/messagebus

# Taken from rc-scripts
is_yes()
{
	# Check value
	case "$1" in
	  yes|Yes|YES|true|True|TRUE|on|On|ON|Y|y|1)
		# true returns zero
		return 0
		;;
	  *)
		# false returns one
		return 1
		;;
	esac
}

if [ -z "$DBUS_SESSION_BUS_ADDRESS" ] && is_yes "${SESSION_BUS_X_SESSION}"; then
	eval `dbus-launch --sh-syntax --exit-with-session`
fi

unset -f is_yes
