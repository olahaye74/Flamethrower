%define name            flamethrower
%define version         0.1.8
%define release         3
%define prefix          /usr

Name: %name
Version: %version
Release: %release
License: GPL
Summary: Flamethrower
URL: http://systemimager.org
Group: Applications/System
Source: %{name}-%{version}.tar.bz2
BuildArch: noarch
Requires: /usr/bin/perl, udpcast
Vendor: http://sisuite.org
Packager: SIS Devel Team <sisuite-devel@lists.sf.net>
Prefix: %prefix
Buildroot: /tmp/%{name}-%{version}-root
AutoReqProv: no

%description
Multicast file transfer utility.

%prep
%setup

%build
%{__perl} Makefile.PL PREFIX=%{_prefix}
%{__make} %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT
%{__make} install                    CONFDIR=$RPM_BUILD_ROOT DESTDIR=$RPM_BUILD_ROOT
rm -rf                          $RPM_BUILD_ROOT%{prefix}/lib/flamethrower/auto/
find                            $RPM_BUILD_ROOT%{prefix} -name perllocal.pod | xargs rm -f
find                            $RPM_BUILD_ROOT%{prefix} -name .packlist | xargs rm -f

%files
%defattr(-,root,root)
%{prefix}/bin/flamethrower
%{prefix}/bin/flamethrowerd
%{prefix}/lib/flamethrower/*
%doc HOWTO README COPYING CREDITS
%config /etc/flamethrower/flamethrower.conf
%config /etc/init.d/flamethrower-server
%dir /var/lib/flamethrower

%post

%preun

%changelog
* Wed Jun 08 2022 Olivier Lahaye <olivier.lahaye@cea.fr>
- statedir is now /var/run (thus not packaged anymore)
* Fri Sep 21 2012 Olivier Lahaye <olivier.lahaye@cea.fr>
- Fixed install using DESTDIR and using PREFIX for Makefile.PL
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
