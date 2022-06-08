use ExtUtils::MakeMaker;
use Carp;

my $install = "./utils/install-N-sub --config ./utils/install-N-sub.conf";
my $version = `cat VERSION`;
chomp $version;

sub MY::postamble {
    my $string = <<EOF;

set_ver::
\tfind \$(DESTDIR)
\t${install} \$(DESTINSTALLSITEBIN)/flamethrower
\t${install} \$(DESTINSTALLSITEBIN)/flamethrowerd
\t${install} \$(DESTINSTALLSITELIB)/Flamethrower.pm

install_configs::
\tinstall -d \$(CONFDIR)/etc/init.d/
\tinstall -d \$(CONFDIR)/etc/flamethrower/
\tinstall -d \$(CONFDIR)/var/lib/flamethrower/
\tinstall -m 644 etc/flamethrower.conf \$(CONFDIR)/etc/flamethrower/
\tinstall -m 755 etc/init.d/flamethrower-server \$(CONFDIR)/etc/init.d/

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
              'NAME' => 'Flamethrower',
              'EXE_FILES' => [qw(bin/flamethrowerd bin/flamethrower)],
              'dist' => {
                          'COMPRESS'  => 'bzip2 -f',
                          'SUFFIX'    => 'bz2'
                        },
              'PREREQ_PM' => {
                              AppConfig => '1.52',
                        },
              'realclean'   => {FILES => "*.old *.bak *.tar.bz2 *.tar *.tar.gz Makefile"},
             );
