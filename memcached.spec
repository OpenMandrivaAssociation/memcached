Summary:	High-performance memory object caching system
Name:		memcached
Version:	1.4.13
Release:	2
License:	BSD
Group:		System/Servers
URL:		http://memcached.org/
Source0:	http://memcached.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:	memcached.sysconfig
Source3:	memcached.logrotate
Source4:	memcached.service
# (cg) The test profileing stuff doesn't work
Patch0:		0001-Disable-test-profiling-as-it-doesn-t-seem-to-work.patch
Patch2:		memcached-1.4.5-disable-werror.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre):  rpm-helper
Requires(postun): rpm-helper
Requires:	cyrus-sasl sasl-plug-plain sasl-plug-crammd5
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libevent-devel
BuildRequires:	libsasl-devel cyrus-sasl sasl-plug-plain sasl-plug-crammd5
# Required by test suite
BuildRequires:	sasl-plug-sasldb
BuildRequires:	libxslt-proc
BuildRequires:	perl-devel

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
%patch2 -p0 -b .werror

%build
autoreconf -fi
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


%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4.13-2
+ Revision: 795231
- sync slightly with mageia
- drop the sysv script

* Wed Feb 08 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.4.13-1
+ Revision: 771877
- version update 1.4.13

* Sat Nov 12 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.10-1
+ Revision: 730247
- 1.4.10

* Sat Nov 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.9-1
+ Revision: 720367
- 1.4.9

* Sun Aug 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.7-2
+ Revision: 695961
- disable the tests for now

* Sun Aug 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.7-1
+ Revision: 695959
- 1.4.7

* Wed Aug 10 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.6-1
+ Revision: 693825
- 1.4.6

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 1.4.5-7
+ Revision: 669920
- disable werror

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-6mdv2011.0
+ Revision: 627635
- don't force the usage of automake1.7

* Wed Dec 22 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-5mdv2011.0
+ Revision: 623867
- rebuilt against libevent 2.x

* Wed Nov 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.5-4mdv2011.0
+ Revision: 598316
- fix build (fedora)

* Mon May 03 2010 Colin Guthrie <cguthrie@mandriva.org> 1.4.5-3mdv2010.1
+ Revision: 541718
- Fix typo and program name in status output
- Rewrite init script to support multiple instances.
- Fix the case where you want memcached to listen on all network interfaces

* Thu Apr 22 2010 Colin Guthrie <cguthrie@mandriva.org> 1.4.5-1mdv2010.1
+ Revision: 537935
- New version: 1.4.5
- Disable test profiling as it seems to break build.
- Remove check for daemon binary in init script. It's part of the same package.

* Tue Feb 23 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.4.4-2mdv2010.1
+ Revision: 509869
- add missing buildrequires required for test suite and enable it as well
- fix incorrect group for devel package
- fix > 80 character width description for -devel package
- rewrite init script
- don't enable unix sockets / disable networking by default anymore
- cleaned up spec

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.4-1mdv2010.1
+ Revision: 475222
- 1.4.4

* Sun Nov 08 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-1mdv2010.1
+ Revision: 462976
- 1.4.3
- new url
- simplify the initscript and config file
- fix deps

* Sun Oct 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.2-1mdv2010.0
+ Revision: 459200
- 1.4.2

* Sat Sep 19 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4.1-1mdv2010.0
+ Revision: 444621
- 1.4.1
- drop repcached. maybe reintroduce it later

* Sun Jun 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.8-1mdv2010.0
+ Revision: 383709
- 1.2.8
- repcached-2.2-1.2.8
- drop upstream patches
- temporary disable "make test"
- fix deps

* Mon May 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-5mdv2010.0
+ Revision: 371632
- P1: security fix for CVE-2009-1255

* Mon Jan 05 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-4mdv2009.1
+ Revision: 325075
- repcached-2.2

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-3mdv2009.1
+ Revision: 315234
- rebuild

* Wed Aug 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-2mdv2009.0
+ Revision: 276664
- repcached-2.1

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-1mdv2009.0
+ Revision: 270210
- 1.2.6
- rediffed the latest repcached-2.0 patch

* Sat Jun 28 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-3mdv2009.0
+ Revision: 229679
- hardcode %%{_localstatedir}

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Wed May 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-2mdv2009.0
+ Revision: 207045
- rebuilt against libevent-1.4.4

* Thu Apr 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-1mdv2009.0
+ Revision: 192539
- 1.2.5
- rediffed and adjusted repcached-1.2-1.2.4.patch slightly
- fix lib64 stuff
- use --enable-64bit on x86_64

* Thu Feb 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-1mdv2008.1
+ Revision: 173417
- 1.2.4
- new repcached patch (1.1)
- drop upstream implemented patches

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-2mdv2008.1
+ Revision: 109084
- added upstream socket permission fix (P0)
- added replication support (P1)
- added pid file generation fix from fedora (P2)
- major initscript and config rework

* Wed Aug 22 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-1mdv2008.0
+ Revision: 68952
- 1.2.3

* Mon Jul 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2mdv2008.0
+ Revision: 52533
- use the %%serverbuild macro

* Sat May 19 2007 David Walluck <walluck@mandriva.org> 1.2.2-1mdv2008.0
+ Revision: 28446
- 1.2.2
- LSB-complaint and MDV-complaint initscript

* Fri Apr 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-1mdv2008.0
+ Revision: 18625
- 1.2.1


* Tue Dec 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-3mdv2007.0
+ Revision: 100284
- release bump due to #27632
- fix deps (libnet1.1.2-devel)
- fix deps (perl-devel)
- rebuild
- 1.2.0
- fix deps
- bunzip sources
- Import memcached

* Sat Jun 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.12-4mdv2007.0
- fix deps

* Mon Apr 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.12-3mdk
* Fri Mar 17 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.12-2mdk
- rebuilt against libnet1.1.2

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1.1.12-1mdk
- 1.1.12
- fix deps

* Wed May 11 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.11-2mdk
- add prereq on rpm-helper
- rebuild for new libevent

* Sun Jan 23 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.11-1mdk
- initial Mandrakelinux package

