Summary:     Display new system news at login.
Summary(pl): Wy¶wietla nowinki systemowe tu¿ po zalogowaniu siê.
Name:        sysnews
Version:     0.9
Release:     1
Copyright:   GPL
Source:      %{name}-%{version}.tar.gz
Patch:       %{name}-%{version}.pld.diff
Group:       Utilities/System
Requires:    sh-utils
BuildRoot:   /tmp/%{name}-%{version}-buildroot

%description
The news command keeps you informed of news concerning the system.
Each news item is contained in a separate file in the /var/sysnews
directory. Anyone having write permission to this directory can create
a news file.

%description -l pl
Komenda news informuje Ciê o nowo¶ciach dotycz±cych systemu.
Ka¿da wiadomo¶æ znajduje siê w osobnym pliku w katalogu /var/sysnews.
Wszyscy u¿ytkownicy maj±cy prawo pisania do tego katalogu bed± mogli
zostawiæ nowinkê.

%prep
%setup -q
%patch -p1

%build
make CFLAGS="-Wall $RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/sysnews,etc/profile.d,etc/cron.daily,usr/{bin,man/man1}}

make PREFIX=$RPM_BUILD_ROOT/usr install

cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.sh
if [ -t ]; then
     if [ ! -f \$HOME/.news_time ]; then
	cat <<-NEWUSER

	Tip:	Use "news" command to view system news when
	        available. See "man news" for more details.

	NEWUSER
     fi
     news -s
fi
EOF
cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.csh
/usr/bin/tty -s >& /dev/null
if ( ! \$status ) then
   if (! -f ~/.news_time ) then
	cat <<NEWUSER

Tip:	Use "news" command to view system news when
        available. See "man news" for more details.

NEWUSER
   endif
   news -s
endif
EOF

cat <<EOF >$RPM_BUILD_ROOT/etc/cron.daily/sysnews
#!/bin/sh
#
# expire sysnews messages
#
PATH="/bin:/usr/bin:/sbin:/usr/sbin"
FS=""
export PATH FS

news -e 45 -x NEWUSERS,POLICY

#eof
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, man)
%attr(755, root, root) /usr/bin/news
%attr(644, root, man ) /usr/man/man1/news.1
%attr(755, root, root) /etc/profile.d/news.sh
%attr(755, root, root) /etc/profile.d/news.csh
%attr(700, root, root) /etc/cron.daily/sysnews
%dir /var/sysnews
%doc README

%changelog
* Thu Nov 12 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.9-1]
- added using $RPM_OPT_FLAGS on compile time.

* Wed Sep 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
- added %defattr,
- minor modifications of the spec file.

* Mon Sep 28 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- updated to new version,
- BuildRooted,
- added -q to setup,
- added %attr.

* Mon May 29 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- new package version,
- added patch from Debian's version of sysnews.
