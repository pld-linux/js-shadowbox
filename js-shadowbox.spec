Summary:	Web-based media viewer
Name:		js-shadowbox
Version:	3.0.3
Release:	1
License:	Shadowbox License 1.0
Group:		Applications/WWW
# Source0Download: http://www.shadowbox-js.com/download.html
Source0:	shadowbox-%{version}.tar.gz
# Source0-md5:	3ba136b7a110f46f6caeceb9ec8d3093
URL:		http://www.shadowbox-js.com/
Requires:	webapps
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		shadowbox
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Shadowbox is a web-based media viewer application that supports all of
the web's most popular media publishing formats.

Shadowbox is written entirely in JavaScript and CSS and is highly
customizable. Using Shadowbox, website authors can showcase a wide
assortment of media in all major browsers without navigating users
away from the linking page.

%prep
%setup -q -n %{_webapp}-%{version}

# Apache config
cat > apache.conf <<'EOF'
Alias /js/%{_webapp}/ %{_appdir}/
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/%{_webapp}/" => "%{_appdir}/",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a *.js *.css *.png *.gif $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc LICENSE
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
