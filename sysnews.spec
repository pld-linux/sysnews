Summary:	Display new system news at login.
Summary(pl):	Wy¶wietla nowinki systemowe tu¿ po zalogowaniu siê.
Name:		sysnews
Version:	0.9
Release:	2
Copyright:	GPL
Source:		%{name}-%{version}.tar.gz
Patch:		%{name}-%{version}.pld.patch
Group:		Utilities/System
Group(pl):	Narzêdzia/Systemowe
Requires:	sh-utils
BuildRoot:	/tmp/%{name}-%{version}-root

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
install -d $RPM_BUILD_ROOT/{var/sysnews,etc/profile.d,etc/cron.daily,%{_bindir},%{_mandir}/man1}

make install PREFIX=$RPM_BUILD_ROOT/usr

cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.sh
if [ -t ]; then
     if [ ! -f \$HOME/.news_time ]; then
	cat <<-NEWUSER

	Tip:	Use "news" command to view system news when
	        available. See "man news" for more details.

	NEWUSER
     fi
     news -l -p
fi
EOF
cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.csh
%{_bindir}/tty -s >& /dev/null
if ( ! \$status ) then
   if (! -f ~/.news_time ) then
	cat <<NEWUSER

Tip:	Use "news" command to view system news when
        available. See "man news" for more details.

NEWUSER
   endif
   news -l -p
endif
EOF

cat <<EOF >$RPM_BUILD_ROOT/etc/cron.daily/sysnews
#!/bin/sh
#
# expire sysnews messages
#
PATH="/bin:%{_bindir}:/sbin:%{_sbindir}"
FS=""
export PATH FS

news -e 45 -x NEWUSERS,POLICY

#eof
EOF

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/* README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_bindir}/news
%{_mandir}/man1/*
%attr(755,root,root) /etc/profile.d/*
%attr(700,root,root) /etc/cron.daily/sysnews
%attr(755,root,root) %dir /var/sysnews
