%define		plugin		tablecalc
Summary:	DokuWiki tablecalc plugin
Summary(pl.UTF-8):	Wtyczka tablecalc dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20100413
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://narezka.ru/cfd/msgdb/740/tablecalc.zip
# Source0-md5:	fee18e13077ca5bba28165e4e4e68b8e
URL:		http://wiki.splitbrain.org/plugin:tablecalc
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	unzip
Requires:	dokuwiki >= 20061106
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

# 13-04-10
version=$(awk -F"'" '/date/{split($4, a, "-"); printf("%04d-%02d-%02d\n", 2000 + a[3], a[2], a[1])}' syntax.php)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

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
