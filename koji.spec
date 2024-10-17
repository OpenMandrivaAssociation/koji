
Name: koji
Version: 1.7.0
Release: 2
License: LGPLv2 and GPLv2+
# koji.ssl libs (from plague) are GPLv2+
Summary: Build system tools
Group: System/Configuration/Packaging
URL: https://fedorahosted.org/koji
Patch0: fedora-config.patch

Source: https://fedorahosted.org/released/koji/koji-%{version}.tar.bz2
BuildArch: noarch
Requires: python-krbV >= 1.0.13
Requires: python-rpm
Requires: pyOpenSSL
Requires: python-urlgrabber
BuildRequires: python

%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.

%package hub
Summary: Koji XMLRPC interface
Group: System/Configuration/Packaging
License: LGPLv2 and GPLv2
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: apache-mod_wsgi
Requires: postgresql-plpython
Requires: %{name} = %{version}-%{release}

%description hub
koji-hub is the XMLRPC interface to the koji database

%package hub-plugins
Summary: Koji hub plugins
Group: System/Configuration/Packaging
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hub = %{version}-%{release}

%description hub-plugins
Plugins to the koji XMLRPC interface

%package builder
Summary: Koji RPM builder daemon
Group: System/Configuration/Packaging
License: LGPLv2 and GPLv2+
#mergerepos (from createrepo) is GPLv2+
Requires: %{name} = %{version}-%{release}
Requires: mock
Requires(post): chkconfig
Requires(post): initscripts
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(pre): shadow-utils
Requires: cvs
Requires: subversion
Requires: git
Requires: rpm-build
Requires: rpm-mandriva-setup-build
Requires: pykickstart                                                                               
Requires: python-pycdio
Requires: python-cheetah
Requires: createrepo

%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.

%package vm
Summary: Koji virtual machine management daemon
Group: System/Configuration/Packaging
License: LGPLv2
Requires: %{name} = %{version}-%{release}
Requires(post): chkconfig
Requires(post): initscripts
Requires(preun): chkconfig
Requires(preun): initscripts
Requires: python-libvirt
Requires: python-libxml2
Requires: python-virtinst
Requires: qemu-img

%description vm
koji-vm contains a supplemental build daemon that executes certain tasks in a
virtual machine. This package is not required for most installations.

%package utils
Summary: Koji Utilities
Group: System/Configuration/Packaging
Requires: postgresql-plpython
Requires: %{name} = %{version}-%{release}

%description utils
Utilities for the Koji system

%package web
Summary: Koji Web UI
Group: System/Configuration/Packaging
Requires: httpd
Requires: apache-mod_wsgi
Requires: apache-mod_auth_kerb
Requires: postgresql-plpython
Requires: python-cheetah
Requires: %{name} = %{version}-%{release}
Requires: python-krbV >= 1.0.13

%description web
koji-web is a web UI to the Koji system.

%prep
%setup -q
%patch0 -p1 -b .orig

%build

%install
make DESTDIR=$RPM_BUILD_ROOT install

%files
%{_bindir}/*
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/koji.conf
%doc docs Authors COPYING LGPL

%files hub
%{_datadir}/koji-hub
%{_prefix}/libexec/koji-hub/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/kojihub.conf
%config(noreplace) %{_sysconfdir}/koji-hub/hub.conf

%files hub-plugins
%dir %{_prefix}/lib/koji-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py*
%dir %{_sysconfdir}/koji-hub/plugins/
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/messagebus.conf
%config(noreplace) %{_sysconfdir}/koji-hub/plugins/rpm2maven.conf

%files utils
%{_sbindir}/kojira
%{_sbindir}/koji-gc
%{_sbindir}/koji-shadow
%{_initrddir}/kojira
%config(noreplace) %{_sysconfdir}/sysconfig/kojira
%dir %{_sysconfdir}/kojira
%config(noreplace) %{_sysconfdir}/kojira/kojira.conf
%dir %{_sysconfdir}/koji-gc
%config(noreplace) %{_sysconfdir}/koji-gc/koji-gc.conf
%config(noreplace) %{_sysconfdir}/koji-shadow/koji-shadow.conf

%files web
%{_datadir}/koji-web
%dir %{_sysconfdir}/kojiweb
%config(noreplace) %{_sysconfdir}/httpd/conf.d/kojiweb.conf
%config(noreplace) %{_sysconfdir}/kojiweb/web.conf

%files builder
%{_sbindir}/kojid
%{_initrddir}/kojid
%{_prefix}/libexec/kojid/
%config(noreplace) %{_sysconfdir}/sysconfig/kojid
%dir %{_sysconfdir}/kojid
%config(noreplace) %{_sysconfdir}/kojid/kojid.conf
%attr(-,kojibuilder,kojibuilder) /etc/mock/koji

%pre builder
/usr/sbin/useradd -r -s /bin/bash -G mock -d /builddir -M kojibuilder 2>/dev/null ||:

%post builder
/sbin/chkconfig --add kojid
/sbin/service kojid condrestart &> /dev/null || :

%preun builder
if [ $1 = 0 ]; then
  /sbin/service kojid stop &> /dev/null
  /sbin/chkconfig --del kojid
fi

%files vm
%{_sbindir}/kojivmd
%{_datadir}/kojivmd
%{_initrddir}/kojivmd
%config(noreplace) %{_sysconfdir}/sysconfig/kojivmd
%dir %{_sysconfdir}/kojivmd
%config(noreplace) %{_sysconfdir}/kojivmd/kojivmd.conf

%post vm
/sbin/chkconfig --add kojivmd

%preun vm
if [ $1 = 0 ]; then
  /sbin/service kojivmd stop &> /dev/null
  /sbin/chkconfig --del kojivmd
fi

%post utils
/sbin/chkconfig --add kojira
/sbin/service kojira condrestart &> /dev/null || :
%preun utils
if [ $1 = 0 ]; then
  /sbin/service kojira stop &> /dev/null || :
  /sbin/chkconfig --del kojira
fi


%changelog
* Wed Aug 29 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.7.0-1
+ Revision: 816018
- Import koji
- Import koji

