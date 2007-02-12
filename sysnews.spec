Summary:	Display new system news at login
Summary(pl.UTF-8):   Wyświetla nowinki systemowe tuż po zalogowaniu się
Name:		sysnews
Version:	0.9
Release:	8
License:	GPL
Group:		Applications/System
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/admin/login/news-%{version}.tgz
# Source0-md5:	ecce2ac4499d87e1e34bc5178066fdbd
Patch0:		%{name}-pld.patch
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	sh-utils
Provides:	group(sysnews)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The news command keeps you informed of news concerning the system.
Each news item is contained in a separate file in the /var/lib/sysnews
directory. Anyone having write permission to this directory can create
a news file.

%description -l pl.UTF-8
Komenda news informuje Cię o nowościach dotyczących systemu. Każda
wiadomość znajduje się w osobnym pliku w katalogu /var/lib/sysnews.
Wszyscy użytkownicy mający prawo pisania do tego katalogu będą mogli
zostawić nowinkę.

%prep
%setup -q -c
%patch0 -p1

%build
%{__make} CFLAGS="-Wall %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{var/lib/sysnews,etc/profile.d,etc/cron.daily,%{_bindir},%{_mandir}/man1}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

cat <<'EOF' >$RPM_BUILD_ROOT/etc/profile.d/news.sh
if [ -t ]; then
	if [ ! -f $HOME/.news_time ]; then
	cat <<-NEWUSER

Tip:		Use "news" command to view system news when
		available. See "man news" for more details.

NEWUSER
	fi
	news -l
fi
EOF
cat <<'EOF' >$RPM_BUILD_ROOT/etc/profile.d/news.csh
%{_bindir}/tty -s >& /dev/null
if ( ! $status ) then
	if (! -f ~/.news_time ) then
		cat <<NEWUSER

Tip:		Use "news" command to view system news when
		available. See "man news" for more details.

NEWUSER
	endif
	news -l
endif
EOF

cat <<'EOF' >$RPM_BUILD_ROOT/etc/cron.daily/sysnews
#!/bin/sh
#
# expire sysnews messages
#
PATH="/bin:%{_bindir}:/sbin:%{_sbindir}"
FS=""
export PATH FS

news -e 45 -x NEWUSERS,POLICY
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 102 sysnews

%postun
if [ "$1" = "0" ]; then
	%groupremove sysnews
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/news
%{_mandir}/man1/*
%attr(755,root,root) /etc/profile.d/*
%attr(700,root,root) /etc/cron.daily/sysnews
%attr(775,root,sysnews) %dir /var/lib/sysnews
