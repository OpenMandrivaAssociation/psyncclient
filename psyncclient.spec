Summary:       ROSA Sync client
Name:          psyncclient
Version:       0.1
Release:       73
License:       GPLv3
Group:         Graphical desktop/KDE
URL:           http://2safe.com
Source:        %{name}-%{version}.tar.gz
Requires:      %{_lib}psync = %{version}-%{release}
Requires:      %{_lib}config9 >= 1.4.8
Requires:      %{_lib}jsoncpp0 >= 0.5.0
Requires:      %{_lib}curl4 >= 7.26.0
Requires:      kdebase4-workspace >= 4.8.1
BuildRequires: qt4-devel
BuildRequires: kdelibs4-devel
BuildRequires: kdebase4-devel
BuildRequires: %{_lib}jsoncpp-devel
BuildRequires: %{_lib}curl-devel
#BuildRequires: libuuid-devel
#BuildRequires: libneon-devel
BuildRequires: %{_lib}config-devel


%description
Desktop client to synchronization user's data. ROSA Sync client.

%files 
%define kde_path /usr
%define _datadir %kde_path/share
%define _sysconfdir /etc
%define _libdir %kde_path/%{_lib}
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/skel/.psyncclient/sync.cfg
#{_sysconfdir}/skel/.sync-unresolved
%{_datadir}/autostart/psyncnotify.desktop
%{_datadir}/autostart/psyncd.desktop
%{_datadir}/apps/psyncnotify/psyncnotify.notifyrc
%{_datadir}/icons/hicolor/128x128/apps/sync.png
%{_datadir}/icons/hicolor/112x112/apps/sync.png
%{_datadir}/icons/hicolor/96x96/apps/sync.png
%{_datadir}/icons/hicolor/72x72/apps/sync.png
%{_datadir}/icons/hicolor/64x64/apps/sync.png
%{_datadir}/icons/hicolor/48x48/apps/sync.png
%{_datadir}/icons/hicolor/32x32/apps/sync.png
%{_datadir}/icons/hicolor/24x24/apps/sync.png
%{_datadir}/icons/hicolor/22x22/apps/sync.png
%{_datadir}/icons/hicolor/16x16/apps/sync.png
%{_datadir}/icons/gray_icon.png
%{_datadir}/icons/green_icon.png
%{_datadir}/kde4/services/kcm_sync.desktop
%{_datadir}/kde4/services/syncfileitemplugin.desktop
%{_libdir}/kde4/kcm_sync.so
%{_libdir}/kde4/syncfileitemplugin.so
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/psyncconfig.po
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/psyncconfig.mo
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/psyncnotify.po
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/psyncnotify.mo
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/syncfileitemplugin.po
%lang(ru_RU) %{_datadir}/locale/ru/LC_MESSAGES/syncfileitemplugin.mo

#-------------------------------------------------------------------------------

%define major_psync 1
%define libpsync %mklibname psync
#define __find_requires /usr/{_lib}/rpm/mandriva/find-requires
%undefine __find_requires
      
%package -n %libpsync
Group:          Graphical desktop/KDE
Summary:        ROSA Sync client
Obsoletes:      %{_lib}psync < %{version}-%{release}
Obsoletes:      %{_lib}psync1 < %{version}-%{release}

%description -n %libpsync
Rosa Sync library package

%files -n %libpsync
%{_libdir}/libpsync.so.%{major_psync}*
#{_libdir}/libcfg.so
%{_libdir}/liblcfg.so.%{major_psync}*
%{_libdir}/libsync_db.so.%{major_psync}*
%{_libdir}/libsyncdbus.so.%{major_psync}*

#-------------------------------------------------------------------------------

%define develname %mklibname -d psync

%package -n     %develname
Group:          Development/KDE and Qt
Summary:        Rosa Sync library development files
Provides:       %name-devel = %version-%release
Requires:       %libpsync = %version-%release
Obsoletes:      %{_lib}psync-devel < %{version}-%{release}

%description -n %develname
Development files for Rosa Sync

%files -n %develname

#{_libdir}/libcfg.a
%{_includedir}/psync/*
%{_libdir}/liblcfg.so
%{_libdir}/libpsync.so
%{_libdir}/libsync_db.so
%{_libdir}/libsyncdbus.so

#--------------------------------------------------------------------

%prep
%setup -c -q

%build

sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./liblcfg/liblcfg.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libsync_db/libsync_db.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libpsync/libpsync.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./psyncconfig/psyncconfig.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./syncconfigapp/psyncconfig.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./dolphin-plugin/syncfileitemplugin.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libsyncdbus/libsyncdbus.pro

mkdir -p .lib
#make -C libcfg
#cp libcfg/libcfg.so .lib

cd liblcfg
qmake liblcfg.pro
cd ..
%make -C liblcfg
cp liblcfg/liblcfg.so.1.0.0 .lib

cd .lib
ln -s liblcfg.so.1.0.0 liblcfg.so.1.0
ln -s liblcfg.so.1.0.0 liblcfg.so.1
ln -s liblcfg.so.1.0.0 liblcfg.so
cd ..

cd libsync_db
qmake libsync_db.pro
cd ..
%make -C libsync_db
cp libsync_db/libsync_db.so.1.0.0 .lib

cd .lib
ln -s libsync_db.so.1.0.0 libsync_db.so.1.0
ln -s libsync_db.so.1.0.0 libsync_db.so.1
ln -s libsync_db.so.1.0.0 libsync_db.so
cd ..

cd libsyncdbus
qmake libsyncdbus.pro
cd ..
%make -C libsyncdbus
cp libsyncdbus/libsyncdbus.so.1.0.0 .lib

cd .lib
ln -s libsyncdbus.so.1.0.0 libsyncdbus.so.1.0
ln -s libsyncdbus.so.1.0.0 libsyncdbus.so.1
ln -s libsyncdbus.so.1.0.0 libsyncdbus.so
cd ..

cd libpsync
qmake libpsync.pro
cd ..
%make -C libpsync
cp libpsync/libpsync.so.1.0.0 .lib

cd .lib
ln -s libpsync.so.1.0.0 libpsync.so.1.0
ln -s libpsync.so.1.0.0 libpsync.so.1
ln -s libpsync.so.1.0.0 libpsync.so
cd ..

cd libfilesettings
qmake filesettings.pro
%make
cd ..

cd psyncconfig
qmake psyncconfig.pro
%make
cd ..

cd syncconfigapp
qmake psyncconfig.pro
%make
cd ..

cd psyncnotify
qmake psyncnotify.pro
%make
cd ..

cd dolphin-plugin
qmake syncfileitemplugin.pro
%make
cd ..

### For update from 755 to now
cd install_update
qmake install_update.pro
%make
cd ..

make -C syncd


%install
#make PREFIX=buildroot{_libdir} -C libcfg install
make INSTALL_ROOT=%buildroot -C liblcfg install
make INSTALL_ROOT=%buildroot -C libpsync install
make INSTALL_ROOT=%buildroot -C psyncconfig install
make INSTALL_ROOT=%buildroot -C psyncnotify install
make INSTALL_ROOT=%buildroot -C syncd install
make INSTALL_ROOT=%buildroot -C syncconfigapp install
make INSTALL_ROOT=%buildroot -C libsync_db install
make INSTALL_ROOT=%buildroot -C dolphin-plugin install
make INSTALL_ROOT=%buildroot -C libsyncdbus install
make INSTALL_ROOT=%buildroot -C install_update install
                           
%find_lang psyncconfig psyncnotify syncfileitemplugin
