Summary:	Display new system news at login
Summary(pl):	Wy�wietla nowinki systemowe tu� po zalogowaniu si�
Name:		sysnews
Version:	0.9
Release:	5
License:	GPL
Group:		Applications/System
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	5545a1e9a0d982f97fc81befcee0d11e
#Source0:	ftp://sunsite.unc.edu/pub/Linux/system/admin/login/news-%{version}.tgz
Patch0:		%{name}-pld.patch
Requires:	sh-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The news command keeps you informed of news concerning the system.
Each news item is contained in a separate file in the /var/lib/sysnews
directory. Anyone having write permission to this directory can create
a news file.

%description -l pl
Komenda news informuje Ci� o nowo�ciach dotycz�cych systemu. Ka�da
wiadomo�� znajduje si� w osobnym pliku w katalogu /var/lib/sysnews.
Wszyscy u�ytkownicy maj�cy prawo pisania do tego katalogu bed� mogli
zostawi� nowink�.

%prep
%setup -q
%patch -p1

%build
%{__make} CFLAGS="-Wall %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/lib/sysnews,etc/profile.d,etc/cron.daily,%{_bindir},%{_mandir}/man1}

%{__make} install PREFIX=$RPM_BUILD_ROOT%{_prefix}

cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.sh
if [ -t ]; then
	if [ ! -f \$HOME/.news_time ]; then
	cat <<-NEWUSER

Tip:		Use "news" command to view system news when
	        available. See "man news" for more details.

NEWUSER
	fi
	news -l
fi
EOF
cat <<EOF >$RPM_BUILD_ROOT/etc/profile.d/news.csh
%{_bindir}/tty -s >& /dev/null
if ( ! \$status ) then
	if (! -f ~/.news_time ) then
		cat <<NEWUSER

Tip:		Use "news" command to view system news when
		available. See "man news" for more details.

NEWUSER
	endif
	news -l
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

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep -q sysnews /etc/group || (
    /usr/sbin/groupadd -r -f sysnews 1>&2 || :
)

%postun
grep -q sysnews /etc/group && (
    /usr/sbin/groupdel sysnews 1>&2 || :
)

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/news
%{_mandir}/man1/*
%attr(755,root,root) /etc/profile.d/*
%attr(700,root,root) %{_sysconfdir}/cron.daily/sysnews
%attr(775,root,sysnews) %dir /var/lib/sysnews
