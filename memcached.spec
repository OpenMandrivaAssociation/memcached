Summary:	High-performance memory object caching system
Name:		memcached
Version:	1.2.1
Release:	%mkrel 1
License:	BSD
Group:		System/Servers
URL:		http://www.danga.com/memcached/
Source0:	http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
Source1:	memcached.init
Source2:	memcached.sysconfig
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	libnet1.1.2-devel >= 1.1.2
BuildRequires:	libevent-devel
BuildRequires:	automake1.7
BuildRequires:	autoconf2.5
BuildRequires:	perl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
memcached is a flexible memory object caching daemon designed to
alleviate database load in dynamic web applications by storing
objects  in memory. It's based on libevent to scale to any size
needed, and is  specifically optimized to avoid swapping and
always use non-blocking I/O.

%prep

%setup -q

cp %{SOURCE1} memcached.init
cp %{SOURCE2} memcached.sysconfig

%build
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --copy --force && autoconf

%configure2_5x \
    --with-libevent=%{_prefix}

%make

%check
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1

install -m0755 memcached %{buildroot}%{_sbindir}/
install -m0644 doc/memcached.1 %{buildroot}%{_mandir}/man1/
install -m0755 memcached.init %{buildroot}%{_initrddir}/memcached
install -m0644 memcached.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/memcached

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%pre
%_pre_useradd %{name} /dev/null /bin/false

%postun
%_postun_userdel %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc doc/memory_management.txt doc/protocol.txt doc/CONTRIBUTORS.txt
%attr(0755,root,root) %{_initrddir}/memcached
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/memcached
%{_sbindir}/memcached
%{_mandir}/man1/*
