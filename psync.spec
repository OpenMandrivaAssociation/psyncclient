%define LIBDIR $RPM_BUILD_ROOT/usr/lib
%define BINDIR $RPM_BUILD_ROOT/usr/bin
%define TRANSLATEDIR $RPM_BUILD_ROOT/usr/share/locale/ru/LC_MESSAGES
%define ETCDIR $RPM_BUILD_ROOT/etc

Summary: ROSA Sync client
Name: psyncclient
Version: 0.1
Release: 1
License: GPL v.2
Group: Tests
Source:%{name}-%{version}.tar.gz
BuildRoot: /tmp/psync

%description
ROSA Sync client

%prep
%setup -c 

%build
mkdir -p .lib
make -C libcfg
cp libcfg/libcfg.so .lib

cd psyncipclibrary/psyncipclibrary
qmake psyncipclibrary.pro
cd ../..
make -C psyncipclibrary/psyncipclibrary
cp psyncipclibrary/psyncipclibrary/libpsyncipc.so.1.0.0 .lib

cd .lib
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so.1.0
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so.1
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so
cd ..

cd psyncconfig/psyncconfig
qmake psyncconfig.pro
make
cd ../..

cd psyncnotify/psyncnotify
qmake psyncnotify.pro
make
cd ../..

make -C syncd

%install
make PREFIX=$RPM_BUILD_ROOT/usr/lib -C libcfg install
make INSTALL_ROOT=$RPM_BUILD_ROOT -C psyncipclibrary/psyncipclibrary install
make INSTALL_ROOT=$RPM_BUILD_ROOT -C psyncconfig/psyncconfig install
make INSTALL_ROOT=$RPM_BUILD_ROOT -C psyncnotify/psyncnotify install
make INSTALL_ROOT=$RPM_BUILD_ROOT -C syncd install
                           
%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/lib/libcfg.a
/usr/lib/libcfg.so
/usr/lib/libpsyncipc.so
/usr/lib/libpsyncipc.so.1
/usr/lib/libpsyncipc.so.1.0
/usr/lib/libpsyncipc.so.1.0.0
/usr/lib/libpsyncipc.so
/usr/lib/libpsyncipc.so.1
/usr/lib/libpsyncipc.so.1.0
/usr/bin/psyncconfig
/usr/bin/psyncnotify
/usr/bin/psyncd
/usr/bin/psyncctl
/usr/share/locale/ru/LC_MESSAGES/psyncconfig.mo
/usr/share/locale/ru/LC_MESSAGES/psyncnotify.mo
/etc/skel/.psyncclient/cfg/user/default_folder
/etc/skel/.psyncclient/cfg/user/interval
/etc/skel/.psyncclient/cfg/user/sync_is
/etc/skel/.psyncclient/cfg/user/config_lastsync
/etc/skel/.psyncclient/cfg/server/ssl
/etc/skel/.psyncclient/cfg/server/port
/etc/skel/.psyncclient/cfg/server/address
/etc/xdg/autostart/psyncnotify.desktop
/etc/xdg/autostart/psyncd.desktop
