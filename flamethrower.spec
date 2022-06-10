%define name            flamethrower
%define version         $(cat VERSION)
%define release         1

Summary: A multicast file distribution utility
Name: %name
Version: %version
Release: %release
License: GPL
URL: http://systemimager.org
Group: Applications/System
Source: %{name}-%{version}.tar.bz2
BuildArch: noarch
Requires: /usr/bin/perl, udpcast
Vendor: http://sisuite.org
Packager: SIS Devel Team <sisuite-devel@lists.sf.net>
Buildroot: /tmp/%{name}-%{version}-root
# If systemd
%if 0%{?_unitdir:1}
%systemd_requires
%else
Requires: /sbin/chkconfig
%endif
#AutoReq: no

%description
Flamethrower is intended to be an easy to use multicast file distribution
system.  It was created to add multicast install capabilities to
SystemImager, but was designed to be fully functional as a stand-alone
package.

Notable characteristics:
 1)  Works with entire directory hierarchies of files, not just single files.
 2)  Uses a server configuration file that takes module entries that are
     similar to those used by rsyncd.conf.
 3)  Flamethrower is an on-demand system.  The multicast of a module is
     initiated when a client connects, but waits MIN_WAIT (conf file) for
     other clients to connect.  If other clients try to connect after a
     cast has been initiated, they simply wait until that cast has finished,
     and catch the next one when it begins.
 4)  The udpcast package is used as the multicast transport, and offers a
     gob and a half of tuning parameters.Multicast file transfer utility.

%prep
%setup

%build
perl Makefile.PL 
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT
make install             PREFIX=$RPM_BUILD_ROOT%{prefix} PERLPREFIX=$RPM_BUILD_ROOT%{prefix} CONFDIR=$RPM_BUILD_ROOT
rm -rf                          $RPM_BUILD_ROOT%{prefix}/lib/flamethrower/auto/
find                            $RPM_BUILD_ROOT%{prefix} -name perllocal.pod | xargs rm -f

%files
%defattr(-,root,root)
%{_bindir}/flamethrower
%{_bindir}/flamethrowerd
%dir %{prefix}/lib/flamethrower
%{prefix}/lib/flamethrower/*.pm
%doc HOWTO README CREDITS CREDITS
%dir %{_sysconfdir}/flamethrower
%config %{_sysconfdir}/flamethrower/flamethrower.conf
%if 0%{?_unitdir:1}
%{_unitdir}/flamethrower.service
%else
%{_sysconfdir}/init.d/flamethrower-server
%endif
%dir %{_sharedstatedir}/flamethrower
%dir /var/state/flamethrower

%post
# If systemd
%if 0%{?_unitdir:1}
%systemd_post flamethrower
# else not systemd
%else
if [[ -a /usr/lib/lsb/install_initd ]]; then
    /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/flamethrower-server
fi

if [[ -a /sbin/chkconfig ]]; then
    /sbin/chkconfig --add flamethrower-server
fi
# endif systemd
%endif

%preun
# if systemd
%if 0%{?_unitdir:1}
%systemd_preun flamethrower
# else not systemd
%else
if [ $1 = 0 ]; then
        %{_sysconfdir}/init.d/flamethrower-serve rstop

        if [[ -a /usr/lib/lsb/remove_initd ]]; then
            /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/flamethrower-server
        fi

        if [[ -a /sbin/chkconfig ]]; then
            /sbin/chkconfig --del flamethrower-server
        fi
else
        # This is an upgrade: restart the daemon.
        echo "Restarting service..."
        (%{_sysconfdir}/init.d/flamethrower-server status >/dev/null 2>&1 && \
                %{_sysconfdir}/init.d/flamethrower-server restart) || true
fi
# endif systemd/not systemd
%endif

%changelog
* Fri Jun 10 2022 Olivier Lahaye <olivier.lahaye@cea.fr>
- Added support for systemd
- Correctly handle service during upgrade
- verstion is not hardcoded in sepc anymore

* Mon Jan 16 2006 Bernard Li <bli@bcgsc.ca>
- Added %dir /var/lib/flamethrower
* Sat Dec 24 2005 Bernard Li <bli@bcgsc.ca>
- Added PERLPREFIX such that building RPM on systems with newer perl (5.8.5?) works
- PREFIX is needed for backward compatability
- Find the correct perllocal.pod file to delete instead of hardcoding it
* Wed Dec 14 2005 Bernard Li <bli@bcgsc.ca>
- 0.1.7 release
- added directory /var/state/flamethrower needed for /etc/init.d script
* Wed Nov 26 2003 Brian Finley <finley@mcs.anl.gov>
- 0.1.6 release
- simplify spec file
* Thu Jul 03 2003 dann frazier <dannf@dannf.org>
- fix 765028 - stop using %dir macros for system dirs
* Sun Jul 01 2003 dann frazier <dannf@dannf.org>
- first package - based on systeminstaller's .spec file.
