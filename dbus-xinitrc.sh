#! /bin/sh

# Get configuration
. /etc/sysconfig/dbus

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

if is_yes "${SESSION_BUS_X_SESSION}"; then
    if  [ -f /usr/bin/dbus-launch ]; then
	if [ -f /var/run/dbus.pid ]; then
	    if test -z "$DBUS_SESSION_BUS_ADDRESS" ; then
		eval `dbus-launch --sh-syntax --exit-with-session`
	    fi    
	fi
    fi
fi
