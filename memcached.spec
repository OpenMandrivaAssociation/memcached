Summary:	High-performance memory object caching system
Name:		memcached
Version:	1.4.13
Release:	8
License:	BSD
Group:		System/Servers
Url:		http://memcached.org/
Source0:	http://memcached.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:	memcached.sysconfig
Source3:	memcached.logrotate
Source4:	memcached.service
# (cg) The test profileing stuff doesn't work
Patch0:		0001-Disable-test-profiling-as-it-doesn-t-seem-to-work.patch
Patch1:		memcached-automake-1.13.patch
Patch2:		memcached-1.4.5-disable-werror.patch

BuildRequires:	doxygen
BuildRequires:	cyrus-sasl
BuildRequires:	sasl-plug-plain
BuildRequires:	sasl-plug-crammd5
# Required by test suite
BuildRequires:	sasl-plug-sasldb
BuildRequires:	xsltproc
BuildRequires:	sasl-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(libevent)
Requires(post,preun,pre,postun):	rpm-helper
Requires:	cyrus-sasl
Requires:	sasl-plug-plain
Requires:	sasl-plug-crammd5

%description
memcached is a flexible memory object caching daemon designed to alleviate
database load in dynamic web applications by storing objects in memory. It's
based on libevent to scale to any size needed, and is  specifically optimized
to avoid swapping and always use non-blocking I/O.

%package	devel
Summary:	Files needed for development using memcached protocol
Group:		Development/C
Requires:	%{name} = %{version}-%{release}

%description	devel
Install memcached-devel if you are developing C/C++ applications that require
access to the memcached binary include files.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
%serverbuild
%configure2_5x --enable-sasl
%make
make docs

#%%check
#export PATH="$PATH:/sbin:/usr/sbin"
#make test

%install
%makeinstall_std

install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m755 %{SOURCE4} -D %{buildroot}/lib/systemd/system/%{name}.service

install -m755 scripts/%{name}-tool %{buildroot}%{_bindir}/%{name}-tool
install -d %{buildroot}/var/run/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%pre
%_pre_useradd %{name} /dev/null /bin/false

%postun
%_postun_userdel %{name}

%files
%doc AUTHORS* COPYING ChangeLog NEWS README
%doc doc/CONTRIBUTORS doc/protocol.txt doc/readme.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(755,%{name},%{name}) %dir %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
/lib/systemd/system/%{name}.service

%files devel
%dir %{_includedir}/memcached
%{_includedir}/memcached/*.h

