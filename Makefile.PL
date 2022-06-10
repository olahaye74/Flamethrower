use ExtUtils::MakeMaker;
use Carp;

my $install = "./utils/install-N-sub --config ./utils/install-N-sub.conf";
my $version = `cat VERSION`;
chomp $version;

sub MY::postamble {
    my $string = <<EOF;

ifneq ($(wildcard /usr/lib/systemd/system/systemd-halt.service),)
SYSTEMD_OS_UNIT_DIR = /usr/lib/systemd/system
else ifneq ($(wildcard /lib/systemd/system/systemd-halt.service),)
SYSTEMD_OS_UNIT_DIR = /lib/systemd/system
else
SYSTEMD_OS_UNIT_DIR = ""
endif

set_ver::
\t${install} \$(DESTINSTALLSITEBIN)/flamethrower
\t${install} \$(DESTINSTALLSITEBIN)/flamethrowerd
\t${install} \$(DESTINSTALLSITELIB)/Flamethrower.pm
\tchmod 644  \$(DESTINSTALLSITELIB)/Flamethrower.pm


install_configs::
ifneq ("\$(SYSTEMD_OS_UNIT_DIR)","")
\tinstall -d \$(DESTDIR)\$(SYSTEMD_OS_UNIT_DIR)
\tinstall -m644 etc/systemd/flamethrower.service \$(DESTDIR)\$(SYSTEMD_OS_UNIT_DIR)
else
\tinstall -d \$(CONFDIR)/etc/init.d/
\tinstall -m 755 etc/init.d/flamethrower-server \$(CONFDIR)/etc/init.d/
endif
\tinstall -d \$(CONFDIR)/etc/flamethrower/
\tinstall -d \$(CONFDIR)/var/lib/flamethrower/
\tinstall -m 644 etc/flamethrower.conf \$(CONFDIR)/etc/flamethrower/
\t# Handle old distro (no /run, those using initscripts)
\tsed -i -e 's|/run/flamethrower|/var/run/flamethrower|g' \$(CONFDIR)/etc/flamethrower.conf

source_tarball :: tmp/flamethrower-$version.tar.bz2

tmp/flamethrower-$version.tar.bz2::
\tmkdir -p tmp/flamethrower-$version
\ttar -c --exclude tmp/ * | (cd tmp/flamethrower-$version && tar x)
\tcd tmp/flamethrower-$version && rm -rf tmp
\tcd tmp/flamethrower-$version && make clean
\trm -rf \`find tmp/flamethrower-$version -name CVS -type d -printf \"\%p \"\`
\tcd tmp && tar -c flamethrower-$version | bzip2 > flamethrower-$version.tar.bz2

install :: set_ver install_configs

EOF
}


WriteMakefile(
              'VERSION' => $version,
              'NAME' => 'flamethrower',
              'EXE_FILES' => [qw(bin/flamethrowerd bin/flamethrower)],
              'dist' => {
                          'COMPRESS'  => 'bzip2 -f',
                          'SUFFIX'    => 'bz2'
                        },
              'PREREQ_PM' => {
                              AppConfig => '1.52',
                        },
              'realclean'   => {FILES => "*.old *.bak *.tar.bz2 *.tar *.tar.gz Makefile MYMETA.*"},
              # We want to keep flamethrower API private.
              'INSTALLSITELIB' => '$(PREFIX)/lib/flamethrower',
             );
