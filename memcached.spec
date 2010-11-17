Summary:	High-performance memory object caching system
Name:		memcached
Version:	1.4.5
Release:	%mkrel 4
License:	BSD
Group:		System/Servers
URL:		http://memcached.org/
Source0:	http://memcached.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	memcached.init
Source2:	memcached.sysconfig
Source3:	memcached.logrotate
# (cg) The test profileing stuff doesn't work
Patch0:		0001-Disable-test-profiling-as-it-doesn-t-seem-to-work.patch
Patch1:		memcached-1.4.5-issue60.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre):  rpm-helper
Requires(postun): rpm-helper
Requires:	cyrus-sasl sasl-plug-plain sasl-plug-crammd5
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	doxygen
BuildRequires:	libevent-devel
BuildRequires:	libsasl-devel cyrus-sasl sasl-plug-plain sasl-plug-crammd5
# Required by test suite
BuildRequires:	sasl-plug-sasldb
BuildRequires:	libxslt-proc
BuildRequires:	perl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p1 -b .broken-test
%patch1 -p0 -b .issue60

%build
%serverbuild

# (cg) Due to patch0001
aclocal && autoconf && automake --add-missing

%configure2_5x	--enable-sasl
%make
make docs

%check
export PATH="$PATH:/sbin:/usr/sbin"
make test

%install
rm -rf %{buildroot}

%makeinstall_std

install -m755 %{SOURCE1} -D %{buildroot}%{_initrddir}/%{name}
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m644 %{SOURCE3} -D %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS* COPYING ChangeLog NEWS README
%doc doc/CONTRIBUTORS doc/protocol.txt doc/readme.txt doc/threads.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(755,%{name},%{name}) %dir %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-tool
%{_bindir}/%{name}
%{_initrddir}/%{name}
%{_mandir}/man1/%{name}.1*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/memcached
%{_includedir}/memcached/*.h
