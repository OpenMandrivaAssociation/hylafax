%define	major	5
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%define faxspool    %{_var}/spool/fax

Summary:	Sophisticated enterprise strength fax package
Name:		hylafax
Epoch:		1
Version:	5.5.1
Release:	1
License: 	LGPL-style
Group:		Communications
URL: 		http://hylafax.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/hylafax/%{name}-%{version}.tar.gz
Source1:	hylafax-v4.1-cron_entries.tar.bz2
Source2:	hylafax-v4.1-defaults.tar.bz2
Source3:	hylafax-v4.1-dialrules_extras.tar.bz2
Source6: 	hylafax-v4.1-logrotate
Source7:	hylafax-v4.1.1-init
Source8:  	hylafax-v4.1.1-hyla.conf
Patch1:		hylafax-4.1.8-ghostscript-location
Patch2:		hylafax-LIBVERSION.diff
Patch3:		hylafax-soname.diff
Patch5:		hylafax-4.2.1-deps.patch
Patch6:		hylafax-4.2.2-ghostscript_fonts.patch
Patch7:		hylafax-no_rpath.diff
Patch9:		hylafax-mailfax.diff
Patch10:	hylafax-5.2.8-format_not_a_string_literal_and_no_format_arguments.diff
Patch11:	hylafax-5.5.0-pass-char-string-rather-than-c++-object.patch

BuildRequires:	ghostscript >= 7.07
BuildRequires:	jbig-devel
BuildRequires:	lcms-devel
BuildRequires:	jpeg-devel
BuildRequires:	pam-devel
BuildRequires:	tiff-devel >= 3.5.7
BuildRequires:	libtiff-progs >= 3.5.7
BuildRequires:	mgetty
BuildRequires:	mgetty-voice
BuildRequires:	openldap-devel
BuildRequires:	sendmail-command
BuildRequires:	sharutils
BuildRequires:	zlib-devel

Requires:	ghostscript >= 7.07
Requires:	gawk >= 3.0.6
Requires:	MailTransportAgent
Requires:	libtiff-progs >= 3.5.7

Conflicts:	mgetty-sendfax
%rename	hylafax-mailgateway

%description
HylaFAX(tm) is a sophisticated enterprise-strength fax package for class 1 and
2 fax modems on unix systems. It provides spooling services and numerous
supporting fax management tools. The fax clients may reside on machines
different from the server and client implementations exist for a number of
platforms including windows.

You need this package if you are going to install hylafax-client and/or hylafax
server.

Most users want mgetty-voice to be installed too.

%package	server
Summary:	The files for the HylaFAX(tm) fax server
Group:		Communications
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires:	%{name}
Requires:	%{name}-client

%description server
HylaFAX(tm) is a sophisticated enterprise-strength fax package for class 1 and
2 fax modems on unix systems. It provides spooling services and numerous
supporting fax management tools. The fax clients may reside on machines
different from the server and client implementations exist for a number of
platforms including windows.

This is the server portion of HylaFAX.

%package	client
Summary: 	The files for the HylaFAX(tm) fax client
Group:		Communications
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires: 	%{name}

%description	client
HylaFAX(tm) is a sophisticated enterprise-strength fax package for class 1 and
2 fax modems on unix systems. It provides spooling services and numerous
supporting fax management tools. The fax clients may reside on machines
different from the server and client implementations exist for a number of
platforms including windows.

This is the client portion of HylaFAX.

%package -n	%{libname}
Summary:	Hylafax libraries
Group:		System/Libraries

%description -n %{libname}
HylaFAX(tm) is a sophisticated enterprise-strength fax package for class 1 and
2 fax modems on unix systems. It provides spooling services and numerous
supporting fax management tools. The fax clients may reside on machines
different from the server and client implementations exist for a number of
platforms including windows.

This is the shared librairies of HylaFAX.

%package -n	%{devname}
Summary:	Hylafax Development libraries
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	%{libname}-devel = %{EVRD}
Obsoletes:	%{libname}-devel
Conflicts:	%{mklibname hylafax 4.1.1}-devel
Conflicts:	%{mklibname hylafax 4.2.0}-devel
Conflicts:	%{mklibname hylafax 4.2.2}-devel
Conflicts:	%{mklibname hylafax 4.2.5}-devel

%description -n	%{devname}
HylaFAX(tm) is a sophisticated enterprise-strength fax package for class 1 and
2 fax modems on unix systems. It provides spooling services and numerous
supporting fax management tools. The fax clients may reside on machines
different from the server and client implementations exist for a number of
platforms including windows.

This is the development librairies for HylaFAX.

%prep
%setup -q -a 1 -a 2 -a 3
%patch1 -p1
# (oe) set the soname
%patch2 -p1 -b .LIBVERSION
%patch3 -p0 -b .soname
%patch5 -p1 -b .deps
%patch6 -p1 -b .ghostscript
%patch7 -p0 -b .no_rpath
%patch9 -p1 -b .mailfax
%patch10 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch11 -p1 -b .c_str~
# path fix
perl -pi -e "s|/usr/local/lib|%{_libdir}|g" configure

cp %{SOURCE6} hylafax-server.logrotate
cp %{SOURCE7} hylafax-server.init
cp %{SOURCE8} hyla.conf

%build
%serverbuild
# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`

# - Can't use the configure macro because does not understand --prefix
# - A patch makes configure not to ask for a confirmation. An alternative would
#   be to use --quiet, but this way all the configure output would be hidden

export STRIP="/bin/true"

export LDFLAGS="%{ldflags}"

./configure \
	--target=%{_target_platform} \
	--with-DIR_BIN=%{_bindir} \
	--with-DIR_SBIN=%{_sbindir} \
	--with-DIR_LIB=%{_libdir} \
	--with-DIR_LIBEXEC=%{_sbindir} \
	--with-DIR_LIBDATA=%{_datadir}/fax \
	--with-DIR_LOCKS=%{_var}/lock \
	--with-DIR_MAN=%{_mandir} \
	--with-PATH_GSRIP=%{_bindir}/gs \
	--with-DBLIBINC=%{_includedir} \
	--with-LIBTIFF="-ltiff -ljpeg -lz -lm" \
	--with-DIR_SPOOL=%{faxspool} \
	--with-AFM=no \
	--with-AWK=%{_bindir}/gawk \
	--with-PATH_VGETTY=/sbin/vgetty \
	--with-PATH_GETTY=/sbin/mgetty \
	--with-PAGESIZE=A4 \
	--with-PATH_DPSRIP=%{faxspool}/bin/ps2fax \
	--with-PATH_IMPRIP=%{_datadir}/fax/psrip \
	--with-SYSVINIT=%{_initrddir}/hylafax \
	--with-INTERACTIVE=no

#	--with-DSO=LINUX \
#	--with-DSOSUF=so.4 \
#	--with-LIBDB=-ldb \

# CFLAGS is set up by the HylaFAX configure script; setting it up here the
# standard way would break things. Since OPTIMIZER is included in CFLAGS
# by the HylaFAX configure system, it's used here in place of CFLAGS
#make CFLAGS="$RPM_OPT_FLAGS"
%make OPTIMIZER="$CFLAGS %{ldflags}" LDFLAGS="\${LDOPTS} \${LDLIBS} %{ldflags}"

%install
export DONT_FIX_EOL=1

install -d -m 755 %{buildroot}%{_sysconfdir}/{logrotate.d,cron.hourly,cron.daily}
install -d -m 755 %{buildroot}%{_initrddir}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_sbindir}
install -d -m 755 %{buildroot}%{_libdir}
install -d -m 755 %{buildroot}%{_datadir}/fax
install -d -m 755 %{buildroot}%{faxspool}/{etc,config/defaults,bin}
install -d -m 755 %{buildroot}%{_mandir}/{man1,man5,man8}

# install: binaries and man pages
# FAXUSER, FAXGROUP, SYSUSER and SYSGROUP are set to the current user to
# avoid warnings about chown/chgrp if the user building the SRPM is not root;
# they are set to the correct values with the RPM attr macro
%makeinstall -e \
	FAXUSER=`id -u` \
	FAXGROUP=`id -g` \
	SYSUSER=`id -u` \
	SYSGROUP=`id -g` \
	BIN=%{buildroot}%{_bindir} \
	SBIN=%{buildroot}%{_sbindir} \
	LIBDIR=%{buildroot}%{_libdir} \
	LIBDATA=%{buildroot}%{_datadir}/fax \
	LIBEXEC=%{buildroot}%{_sbindir} \
	SPOOL=%{buildroot}%{faxspool} \
	MAN=%{buildroot}%{_mandir} \
	INSTALL_ROOT=%{buildroot}

# some hacks
perl -pi -e 's!/usr/etc/inetd.conf!/etc/inetd.conf!g' %{buildroot}%{_sbindir}/faxsetup
perl -pi -e 's!/usr/lib/aliases!/etc/aliases!g' %{buildroot}%{_sbindir}/faxsetup

# Starting from 4.1.6, port/install.sh won't chown/chmod anymore if the current
# user is not root; instead a file root.sh is created with chown/chmod inside.
#
# If you build the rpm as normal user (not root) you get an rpm with all the
# permissions messed up and hylafax will give various weird errors.
#
# The following line fixes that.
#
[ -f root.sh ] && sh root.sh

# init
install -m0755 hylafax-server.init %{buildroot}%{_initrddir}/hylafax-server

# defaults - Disabling this: the defaults are ancient
#install -m 644 defaults/* %{buildroot}%{faxspool}/config/defaults/

# hyla.conf - Need a new default - this one just sets fine mode
#leaving it since it doesn't hurt
install -m0644 hyla.conf %{buildroot}%{_datadir}/fax/hyla.conf

# cron entries - These seem fine
install -m 755 hylafax_daily.cron  %{buildroot}%{_sysconfdir}/cron.daily/hylafax
install -m 755 hylafax_hourly.cron %{buildroot}%{_sysconfdir}/cron.hourly/hylafax

# logrotate
install -m0644 hylafax-server.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/hylafax-server

# dialrules extras - Darren says the dialrules haven't changed
install -m 644 dialrules_extras/dialrules* %{buildroot}%{faxspool}/etc

ln -s ps2fax.gs %{buildroot}%{faxspool}/bin/ps2fax

/sbin/ldconfig -n %{buildroot}%_libdir

# If Linux, what else...? :-), delete unnecessary files
%ifos linux
rm -f %{buildroot}%{_sbindir}/{faxsetup.irix,faxsetup.bsdi}
%endif

chmod +x %{buildroot}{%_sbindir/*,/var/spool/fax/bin/*}

cat > README.urpmi << EOF
#########################################################
#            HylaFAX installation complete!             #
#                                                       #
#      You should now run /usr/sbin/faxsetup to         #
#       create or update HylaFAX configuration          #
#      before you can begin using the software.         #
#                                                       #
#########################################################
EOF

# install the mailfax stuff
install -m0755 faxmail/mailfax.sh-postfix %{buildroot}%{_bindir}/
install -m0755 faxmail/mailfax.sh-qmail %{buildroot}%{_bindir}/
install -m0755 faxmail/mailfax.sh-sendmail %{buildroot}%{_bindir}/
install -m0755 faxmail/mailfax.sh-smail %{buildroot}%{_bindir}/

%post client
%{_sbindir}/faxsetup -client

%post server
%_post_service hylafax-server

# Adding faxgetty entry to %{_sysconfdir}/inittab
logger adding FaxGetty entry to %{_sysconfdir}/inittab
cat %{_sysconfdir}/inittab | grep -i "faxgetty entry" || \
echo -e "# FaxGetty Entry\n#t0:23:respawn:%{_sbindir}/faxgetty ttyS0" >> %{_sysconfdir}/inittab

echo "Please run \"%{_sbindir}/faxsetup -server\" to configure your fax server"

%preun server
%_preun_service hylafax-server

%files
%doc CHANGES CONTRIBUTORS COPYRIGHT INSTALL README TODO VERSION
%{_sbindir}/faxsetup
%{_sbindir}/faxsetup.linux
%attr(-,uucp,uucp) %dir %{faxspool}
%attr(-,uucp,uucp) %dir %{faxspool}/archive
%attr(-,uucp,uucp) %dir %{faxspool}/bin
%attr(-,uucp,uucp) %dir %{faxspool}/client
%attr(-,uucp,uucp) %dir %{faxspool}/config
%attr(-,uucp,uucp) %dir %{faxspool}/dev
%attr(-,uucp,uucp) %dir %{faxspool}/docq
%attr(-,uucp,uucp) %dir %{faxspool}/doneq
%attr(-,uucp,uucp) %dir %{faxspool}/etc
%attr(-,uucp,uucp) %dir %{faxspool}/info
%attr(-,uucp,uucp) %dir %{faxspool}/log
%attr(-,uucp,uucp) %dir %{faxspool}/pollq
%attr(-,uucp,uucp) %dir %{faxspool}/recvq
%attr(-,uucp,uucp) %dir %{faxspool}/sendq
%attr(-,uucp,uucp) %dir %{faxspool}/status
%attr(-,uucp,uucp) %dir %{faxspool}/tmp
%attr(-,uucp,uucp) %{faxspool}/FIFO*
%attr(-,root,root) %{faxspool}/COPYRIGHT

%files server
%doc README.urpmi
%attr(0755,root,root) %{_initrddir}/hylafax-server
%attr(0755,root,root) %{_sysconfdir}/cron.daily/hylafax
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/hylafax
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/hylafax-server
%{_sbindir}/faxlock
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/xferfaxlog
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/hosts.hfaxd
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/lutRS18.pcf
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/dpsprinter.ps
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/cover.templ
%attr(-,uucp,uucp) %config(noreplace) %{faxspool}/etc/dialrules*
#
%{faxspool}/bin/*
%{faxspool}/config/*
%{_sbindir}/hfaxd
%{_sbindir}/hylafax
%{_sbindir}/faxdeluser
%{_sbindir}/faxadduser
%{_sbindir}/choptest
%{_sbindir}/cqtest
%{_sbindir}/dialtest
%{_sbindir}/faxabort
%{_sbindir}/faxaddmodem
%{_sbindir}/faxanswer
%{_sbindir}/faxconfig
%{_sbindir}/faxcron
%{_sbindir}/faxgetty
%{_sbindir}/faxinfo
%{_sbindir}/faxmodem
%{_sbindir}/faxmsg
%{_sbindir}/faxq
%{_sbindir}/faxqclean
%{_sbindir}/faxquit
%{_sbindir}/faxsend
%{_sbindir}/faxstate
%{_sbindir}/faxwatch
%{_sbindir}/lockname
%{_sbindir}/ondelay
%{_sbindir}/pagesend
%{_sbindir}/probemodem
%{_sbindir}/recvstats
%{_sbindir}/tagtest
%{_sbindir}/tiffcheck
%{_sbindir}/tsitest
%{_sbindir}/typetest
%{_sbindir}/xferfaxstats
%{_datadir}/fax/faxmail.ps
%{_datadir}/fax/hfaxd.conf
%{_mandir}/man5/*
%{_mandir}/man8/*

%files client
%doc faxmail/README
%{_bindir}/sendfax
%{_bindir}/sendpage
%{_bindir}/faxstat
%{_bindir}/faxalter
%{_bindir}/faxcover
%{_bindir}/faxmail
%{_bindir}/faxrm
%{_bindir}/mailfax.sh-postfix
%{_bindir}/mailfax.sh-qmail
%{_bindir}/mailfax.sh-sendmail
%{_bindir}/mailfax.sh-smail
%{_sbindir}/textfmt
%{_sbindir}/edit-faxcover
%{_datadir}/fax/pagesizes
%{_datadir}/fax/faxcover.ps
%{_datadir}/fax/typerules
%config(noreplace) %{_datadir}/fax/hyla.conf
%dir %{_datadir}/fax/faxmail
%dir %{_datadir}/fax/faxmail/application
%dir %{_datadir}/fax/faxmail/image
%{_datadir}/fax/faxmail/application/octet-stream
%{_datadir}/fax/faxmail/application/pdf
%{_datadir}/fax/faxmail/image/tiff
%{_mandir}/man1/*

%files -n %{libname}
%doc COPYRIGHT
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc COPYRIGHT
%{_libdir}/*.so


%changelog
* Wed May 30 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:5.5.1-1
+ Revision: 801361
- move spool directory to main package, otherwise faxsetup script will fail for
  client package
- minor cosmetics
- drop dead %%cputoolize macro
- new version

  + Matthew Dawkins <mattydaw@mandriva.org>
    - fixed BRs
    - added fix for serverbuild macro
    - some clean up of spec

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against libtiff.so.5

* Tue Jul 05 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:5.5.0-1
+ Revision: 688911
- enable ldap & lcms support
- really link with %%ldflags
- don't pass build dir to %%setup when it's already the default
- use %%{EVRD} macro
- drop legacy rpm stuff
- ditch workaround for FIFO file in %%post, just include it in %%files now
- fix attempt of passing c++ object rather than c-string to fprintf (P11)
- don't pass tiff arguments to configure script, it breaks it for some reason,
  and it's anyways able to auto-detect this by itself
- ditch no longer required -fPIC patch (P0)
- new version

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.9-3mdv2010.1
+ Revision: 488766
- rebuilt against libjpeg v8

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.9-2mdv2010.0
+ Revision: 416617
- rebuilt against libjpeg v7

* Sun Mar 01 2009 Emmanuel Andry <eandry@mandriva.org> 1:5.2.9-1mdv2009.1
+ Revision: 346377
- New version 5.2.9

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.8-2mdv2009.1
+ Revision: 335842
- rebuilt against new jbigkit major

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.8-1mdv2009.1
+ Revision: 318015
- 5.2.8
- use %%ldflags
- fix build with -Werror=format-security (P10)

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.7-1mdv2009.0
+ Revision: 270190
- 5.2.7

* Mon Jul 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.6-1mdv2009.0
+ Revision: 239499
- 5.2.6

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.5-0.1mdv2009.0
+ Revision: 211357
- 5.2.5
- manually set -Wl,--as-needed -Wl,--no-undefined for now

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.4-1mdv2009.0
+ Revision: 208711
- 5.2.4

* Thu Mar 27 2008 Oden Eriksson <oeriksson@mandriva.com> 1:5.2.0-3mdv2008.1
+ Revision: 190662
- fix build deps
- disable fix_eol because it just hangs

  + Emmanuel Andry <eandry@mandriva.org>
    - Fix lib group
    - protect major

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 1:5.2.0-2mdv2008.1
+ Revision: 157251
- rebuild with fixed %%serverbuild macro

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Dec 27 2007 Jérôme Soyer <saispo@mandriva.org> 1:5.2.0-1mdv2008.1
+ Revision: 138387
- New release

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Nov 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.12-1mdv2008.1
+ Revision: 114004
- 5.1.12

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.11-1mdv2008.1
+ Revision: 107512
- 5.1.11

* Fri Oct 12 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.9-1mdv2008.1
+ Revision: 97562
- 5.1.9 (Minor feature enhancements)
- drop P8, implemented upstream

* Tue Aug 28 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.8-1mdv2008.0
+ Revision: 72878
- 5.1.8
- fix deps (jbig-devel)

* Tue Aug 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.7-2mdv2008.0
+ Revision: 59741
- fix #32347 (hylafax-server depends on hylafax-client but no dependencies are set)

* Mon Aug 06 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.7-1mdv2008.0
+ Revision: 59286
- 5.1.7
- rediffed P2
- removed the last hunk in P8
- obey new devel naming specs

* Mon Jul 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.6-1mdv2008.0
+ Revision: 54555
- revert some stuff with P2 (why do they change this with each release???)
- rediffed P3,P7,P8
- use the new %%serverbuild macro
- make it provide a usefull debug package
- rediffed P3
- 5.1.6

* Sat Jun 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.5-1mdv2008.0
+ Revision: 43447
- 5.1.5

* Sun May 27 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:5.1.4-4mdv2008.0
+ Revision: 31885
- Do not modify the inittab ( close bug #21975)
- Fix group (#28134)

* Sat May 26 2007 Nicolas Lécureuil <nlecureuil@mandriva.com> 1:5.1.4-2mdv2008.0
+ Revision: 31573
- Do not overwrite conf file (#21179)

* Tue May 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.4-1mdv2008.0
+ Revision: 26851
- 5.1.4

* Thu May 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1:5.1.3-1mdv2008.0
+ Revision: 25963
- 5.1.3


* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 5.0.2-1mdv2007.0
+ Revision: 101470
- 5.0.2
- new major (5)
- drop upstream patches; P2
- added P7 to remove rpath from the binaries

* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1:4.3.0-1mdv2007.1
+ Revision: 101452
- Import hylafax

* Wed Jul 26 2006 Oden Eriksson <oeriksson@mandriva.com> 4.3.0-1mdv2007.1
- 4.3.0

* Tue Jun 13 2006 Oden Eriksson <oeriksson@mandriva.com> 4.3.0.3-1mdv2007.0
- 4.3.0.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 4.2.5.2-2mdk
- fix attribs on the cron files (#20975)

* Wed Feb 01 2006 Oden Eriksson <oeriksson@mandriva.com> 4.2.5.2-1mdk
- 4.2.5.2 (includes fixes for CVE-2005-3538 and CVE-2005-3539)
- fixes #16448 and #16527
- html docs are not provided anymore
- re-enabled a rediffed soname patch (P3)
- misc rpmlint and spec file fixes

* Wed Oct 19 2005 Daouda LO <daouda@mandriva.com> 4.2.2-1mdk
- update to official 4.2.2 release
- patch #4 (64 bit fixes) merged upstream 
- spec cleanup 
- fix #16448 #16527

* Thu Sep 08 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 4.2.1-2mdk
- 64-bit fixes
- make it parallel buildable (deps fixes)

* Mon Jun 13 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.2.1-1mdk
- 4.2.1
- drop P13 (merged upstream)
- %%mkrel
- fix requires

* Thu Jan 13 2005 Daouda LO <daouda@mandrakesoft.com> 4.2.0-3mdk
- security fix for CAN-2004-1182
- versionned and bzipped patch

* Sat Jan 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.2.0-2mdk
- added P12 (fix soname)
- hacked the hylafax_daily.cron file to stop try to send mails if the
  hylafax server is not running
- added the same message as in %%post server to the init script
- misc rpmlint fixes

* Sat Sep 04 2004 Daouda LO <daouda@mandrakesoft.com> 4.2.0-1mdk
- release 4.2.0:
  o added Class 1 ECM and MMR support
  o added Class 1.0 V.34-Fax (SuperG3) Support
  o added software-driven real-time format compression conversion
  o added extended resolution support
  o removed the requirement for a case-sensitive filesystem to build
  o unified the queue file numbering mechanism
  o integrated Caller-ID/DID support throughout the software
- * Wed Aug  4 2004 Bill Binko <bill@binko.net> 4.2.0-0.rc2.1mdk
  - 4.2.0 RC2
     o Updated to the Release Candidate
     o renamed RPM per Daouda's advice

* Fri Jan 16 2004 Daouda LO <daouda@mandrakesoft.com> 4.1.8-2mdk
- Good permissions which prevent hylafax from working out of the box.

* Tue Jan 06 2004 Daouda LO <daouda@mandrakesoft.com> 4.1.8-1mdk
- 4.1.8
  o fix PageChop feature (4.1.7)
  o security fix (merged upstream)
  o default libtiff v3.6 compatibility
  o numerous bugfixes (several significant) and build cleanups
- Create fifo files in post install
- add clean section

