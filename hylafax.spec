%global optflags %{optflags} -Wno-format-security

%define __noautoreq '.*/bin/awk|.*/bin/gawk'

%define	major	7
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%define faxspool    %{_var}/spool/fax

Summary:	Sophisticated enterprise strength fax package
Name:		hylafax
Epoch:		1
Version:	6.0.7
Release:	2
License: 	LGPL-style
Group:		Communications
Url: 		https://hylafax.sourceforge.net/
Source0:	ftp://ftp.hylafax.org/source/hylafax-%{version}.tar.gz
Source1:	hylafax-v4.1-cron_entries.tar.bz2
Source2:	hylafax-v4.1-defaults.tar.bz2
Source3:	hylafax-v4.1-dialrules_extras.tar.bz2
Source6: 	hylafax-v4.1-logrotate
Source7:	hylafax-v4.1.1-init
Source8:  	hylafax-v4.1.1-hyla.conf
Patch1:		hylafax-4.1.8-ghostscript-location
Patch5:		hylafax-4.2.1-deps.patch
Patch6:		hylafax-4.2.2-ghostscript_fonts.patch
Patch9:		hylafax-mailfax.diff
Patch10:	hylafax-5.2.8-format_not_a_string_literal_and_no_format_arguments.diff
Patch11:	hylafax-5.5.0-pass-char-string-rather-than-c++-object.patch

BuildRequires:	ghostscript >= 7.07
BuildRequires:	libtiff-progs >= 3.5.7
BuildRequires:	mgetty
BuildRequires:	mgetty-voice
BuildRequires:	sendmail-command
BuildRequires:	sharutils
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	tiff-devel >= 3.5.7
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(zlib)

Requires:	gawk >= 3.0.6
Requires:	ghostscript >= 7.07
Requires:	libtiff-progs >= 3.5.7
Requires:	MailTransportAgent
Obsoletes:	%{devname} < %{EVRD}

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
Requires(post,postun):	rpm-helper
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
Requires(post,preun):	rpm-helper
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

%prep
%setup -q -a 1 -a 2 -a 3
%patch1 -p1
# (oe) set the soname
#patch5 -p1 -b .deps
#patch6 -p1 -b .ghostscript
%patch9 -p1 -b .mailfax
#patch10 -p0 -b .format_not_a_string_literal_and_no_format_arguments
#patch11 -p1 -b .c_str~
# path fix
sed -i -e "s|/usr/local/lib|%{_libdir}|g" configure

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
sed -i -e 's!/usr/etc/inetd.conf!/etc/inetd.conf!g' %{buildroot}%{_sbindir}/faxsetup
sed -i -e 's!/usr/lib/aliases!/etc/aliases!g' %{buildroot}%{_sbindir}/faxsetup

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
%doc CONTRIBUTORS COPYRIGHT INSTALL README TODO VERSION
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
%{faxspool}/etc/templates
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
%{_datadir}/fax/faxcover*.ps
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
%{_mandir}/man1/*

%files -n %{libname}
%doc COPYRIGHT
%{_libdir}/libhylafax-6.0.so.%{major}*
