Summary:	Unix shell embedded within Scheme
Name:		scsh
Version:	0.6.6
Release:	1
License:	BSD-like
Group:		Applications/Shells
URL:		http://www.scsh.net/
Source0:	ftp://ftp.scsh.net/pub/scsh/0.6/%{name}-%{version}.tar.gz
# Source0-md5:	fa0a62f8ec7b0629c297144c59027ba4
Patch0:		%{name}-build.patch
BuildRequires:	automake
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir	/bin

%description
Scsh is a variant of Scheme 48 (an R5RS compliant new-tech Scheme
system) Scsh is designed for writing real-life standalone Unix
programs and shell scripts. Scsh spans a wide range of application,
from ?script? applications usually handled with perl or sh, to more
standard systems applications usually written in C.

%package devel
Summary:	Development scsh files
Group:		Development/Libraries

%description devel
Unix shell embedded within Scheme - development files.

%prep
%setup -q
%patch0 -p1

%build
cp -f %{_datadir}/automake/config.sub .
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{doc,env},%{_includedir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a $RPM_BUILD_ROOT%{_libdir}

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
if [ ! -f /etc/shells ]; then
	echo "%{_bindir}/scsh" >> /etc/shells
else
	grep -q '^%{_bindir}/scsh$' /etc/shells || echo "%{_bindir}/scsh" >> /etc/shells
fi

%preun
if [ "$1" = "0" ]; then
	umask 022
	grep -v '^%{_bindir}/scsh$' /etc/shells > /etc/shells.new
	mv -f /etc/shells.new /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc doc/*/html/* doc/*.txt
%attr(755,root,root) %{_bindir}/scsh
%dir %{_libdir}/scsh
%{_libdir}/scsh/[bcelmor]*
%{_libdir}/scsh/scsh
%{_libdir}/scsh/srfi
%{_libdir}/scsh/*.image
%attr(755,root,root) %{_libdir}/scsh/scshvm
%{_mandir}/man?/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_libdir}/*.a
