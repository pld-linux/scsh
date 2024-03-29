Summary:	Unix shell embedded within Scheme
Summary(pl.UTF-8):	Uniksowa powłoka osadzona w Scheme
Name:		scsh
Version:	0.6.7
Release:	2
License:	BSD-like
Group:		Applications/Shells
#Source0Download: https://scsh.net/download/download.html
Source0:	https://ftp.scsh.net/pub/scsh/0.6/%{name}-%{version}.tar.gz
# Source0-md5:	69c88ca86a8aaaf0f87d253b99d339b5
Patch0:		%{name}-build.patch
Patch1:		%{name}-link.patch
URL:		https://scsh.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.213
Requires(post,preun):	grep
Requires(preun):	fileutils
ExcludeArch:	%{x8664} alpha ia64 ppc64 s390x sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir	/bin

%description
Scsh is a variant of Scheme 48 (an R5RS compliant new-tech Scheme
system). Scsh is designed for writing real-life standalone Unix
programs and shell scripts. Scsh spans a wide range of application,
from "script" applications usually handled with perl or sh, to more
standard systems applications usually written in C.

%description -l pl.UTF-8
scsh to odmiana Scheme 48 (systemu new-tech Scheme zgodnego z R5RS).
scsh zostął zaprojektowany do pisania rzeczywistych, samodzielnych
programów i skryptów powłoki pod Uniksem. scsh obejmuje szeroki zakres
zastosowań, od aplikacji "skryptowych" zwykle obsługiwanych przy
pomocy Perla lub sh do bardziej standardowych aplikacji systemowych
zwykle pisanych w C.

%package devel
Summary:	Development scsh files
Summary(pl.UTF-8):	Programistyczne pliki scsh
Group:		Development/Libraries

%description devel
Unix shell embedded within Scheme - development files.

%description devel -l pl.UTF-8
Pliki programistyczne scsh - uniksowej powłoki osadzonej w Scheme.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub .
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/{doc,env},%{_includedir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.a $RPM_BUILD_ROOT%{_libdir}

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/doc

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
%{_libdir}/scsh/big
%{_libdir}/scsh/cig
%{_libdir}/scsh/env
%{_libdir}/scsh/link
%{_libdir}/scsh/misc
%{_libdir}/scsh/opt
%{_libdir}/scsh/rts
%{_libdir}/scsh/scsh
%{_libdir}/scsh/srfi
%{_libdir}/scsh/*.image
%attr(755,root,root) %{_libdir}/scsh/scshvm
%{_mandir}/man1/scsh.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/scheme48.h
%{_includedir}/write-barrier.h
%{_libdir}/libscsh.a
%{_libdir}/libscshvm.a
