%define		subver	2017-02-09
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		tablecalc
%define		php_min_version 5.3.0
Summary:	DokuWiki tablecalc plugin
Summary(pl.UTF-8):	Wtyczka tablecalc dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://narezka.org/cfd/msgdb/740/tablecalc.zip
# Source0-md5:	6a68227688486e83b8b7a9dd573f4a87
URL:		https://www.dokuwiki.org/plugin:tablecalc
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	unzip
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir	/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%description
Adds ability to use Excel-style formulas in tables.

%prep
%setup -qc
mv %{plugin}/* .

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# 13-04-10
version=$(awk -F"'" '/date/{split($4, a, "-"); printf("%04d-%02d-%02d\n", 2000 + a[3], a[2], a[1])}' syntax.php)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.js
