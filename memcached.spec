Summary:        High-performance memory object caching system
Name:           memcached
Version:        1.2.6
Release:        %mkrel 3
License:        BSD
Group:          System/Servers
URL:            http://www.danga.com/memcached/
Source0:        http://www.danga.com/memcached/dist/%{name}-%{version}.tar.gz
Source1:        memcached.init
Source2:        memcached.sysconfig
Source3:        memcached.logrotate
# http://repcached.lab.klab.org/
# http://downloads.sourceforge.net/repcached/repcached-2.0-1.2.5.patch.gz
Patch0:		repcached/repcached-2.1-1.2.6.patch.gz
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre):  rpm-helper
Requires(postun): rpm-helper
BuildRequires:  automake1.7
BuildRequires:  autoconf2.5
BuildRequires:  libevent-devel
BuildRequires:  libnet1.1.2-devel >= 1.1.2
BuildRequires:  perl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
memcached is a flexible memory object caching daemon designed to alleviate
database load in dynamic web applications by storing objects in memory. It's
based on libevent to scale to any size needed, and is  specifically optimized
to avoid swapping and always use non-blocking I/O.

The memcached server binary comes in two flavours:

 o memcached             - with threading support
 o memcached-replication - with replication support

%prep

%setup -q
%patch0 -p1

cp %{SOURCE1} memcached.init
cp %{SOURCE2} memcached.sysconfig
cp %{SOURCE3} memcached.logrotate

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.*

%build
rm -f configure
libtoolize --copy --force; aclocal; automake --add-missing --copy --foreign; autoheader; autoconf

%serverbuild

%configure2_5x \
%ifarch x86_64
    --enable-64bit \
%endif
    --with-libevent=%{_prefix} \
    --enable-replication

%make
cp -p %{name} _%{name}-replication_

make clean

%configure2_5x \
    --localstatedir=/var/lib \
%ifarch x86_64
    --enable-64bit \
%endif
    --with-libevent=%{_prefix} \
    --enable-threads

%make

#%%check
#%%{__make} test

%install
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}/var/lib/%{name}
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/run/%{name}

install -m0755 %{name} %{buildroot}%{_sbindir}/
install -m0755 _%{name}-replication_ %{buildroot}%{_sbindir}/%{name}-replication
install -m0644 doc/%{name}.1 %{buildroot}%{_mandir}/man1/

install -m0755 memcached.init %{buildroot}%{_initrddir}/%{name}
install -m0644 memcached.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 memcached.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m0755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%pre
%_pre_useradd %{name} /dev/null /bin/false

%postun
%_postun_userdel %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS* COPYING ChangeLog NEWS README TODO
%doc doc/memory_management.txt doc/protocol.txt doc/CONTRIBUTORS
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_bindir}/%{name}-tool
%{_sbindir}/%{name}
%{_sbindir}/%{name}-replication
%{_mandir}/man1/*
%attr(0711,%{name},%{name}) %dir /var/lib/%{name}
%attr(0711,%{name},%{name}) %dir /var/log/%{name}
%attr(0711,%{name},%{name}) %dir /var/run/%{name}
