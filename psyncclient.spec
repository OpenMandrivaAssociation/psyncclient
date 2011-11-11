%define major 1
%define libname %mklibname psync %{major}
%define develname %mklibname -d psync

Summary:       MandrivaSync client
Name:          psyncclient
Version:       0.1
Release:       %mkrel 22
License:       GPLv2
Group:         Graphical desktop/KDE
Source:        %{name}-%{version}.tar.gz
Requires: %{libname} >= %{version}-%{release}
Requires: %{_lib}config9
Requires: %{_lib}openssl1.0.0
BuildRequires: qt4-devel
BuildRequires: kdelibs4-devel
BuildRequires: libuuid-devel
BuildRequires: libneon-devel
BuildRequires: %{_lib}config-devel
BuildRequires: %{_lib}openssl-devel
#BuildRequires: %{_lib}openssl1.0.0-devel
BuildRequires: %{_lib}krb53
Epoch: 1

%description
MandrivaSync client

%files -f psyncconfig.lang
%{_bindir}/*
%{_sysconfdir}/skel/.psyncclient
#%{_sysconfdir}/skel/.sync-unresolved
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
%{_datadir}/kde4/services/kcm_sync.desktop
%{_libdir}/kde4/kcm_sync.so

#-------------------------------------------------------------------------------

      
%package -n %libname
Group:          Graphical desktop/KDE
Summary:        MandrivaSync client
# just wonderful...
# In order to satisfy the 'libpsync.so.1()(64bit)' dependency, one of the following packages is needed:
# 1- lib64psync-0.1-14-mdv2011.0.x86_64: MandrivaSync client (to install)
# 2- lib64psync1-0.1-10-mdv2011.0.x86_64: ROSA Sync client (to install)
# 3- lib641-0.1-8-mdv2011.0.x86_64: ROSA Sync client (to install)
# 4- lib64%major_psync-0.1-6-mdv2011.0.x86_64: ROSA Sync client (to install)
# What is your choice? (1-4) ^C
Obsoletes: %{mklibname psync} >= 0.1
Obsoletes: %{mklibname psyncipc 1} >= 0.1
Obsoletes: %{mklibname 1} >= 0.1
Obsoletes: %{mklibname %major_psync} >= 0.1

%description -n %libname
psync library

%files -n %libname
%{_libdir}/libpsync.so.%{major}*
#%{_libdir}/libcfg.so
%{_libdir}/liblcfg.so.%{major}*
%{_libdir}/liblcfg.so
%{_libdir}/libpsync.so


#-------------------------------------------------------------------------------


%package -n     %develname
Group:          Development/KDE and Qt
Summary:        %name developement files
Provides:       %name-devel = %version-%release
Requires: %{libname} >= %{version}-%{release}
Obsoletes: %{mklibname psyncipc -d}

%description -n %develname
Development files for %name .

%files -n %develname

#%{_libdir}/libcfg.a
%{_includedir}/psync/*

#--------------------------------------------------------------------

%prep
%setup -c -q

%build

sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./liblcfg/liblcfg.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libpsync/libpsync.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./psyncconfig/psyncconfig.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./syncconfigapp/psyncconfig.pro


mkdir -p .lib
#%make -C libcfg
#cp libcfg/libcfg.so .lib


cd liblcfg
qmake liblcfg.pro
cd ..
%make -C liblcfg
cp liblcfg/liblcfg.so.%{major}.0.0 .lib

cd .lib
ln -s liblcfg.so.%{major}.0.0 liblcfg.so.%{major}.0
ln -s liblcfg.so.%{major}.0.0 liblcfg.so.%{major}
ln -s liblcfg.so.%{major}.0.0 liblcfg.so
cd ..

cd libpsync
qmake libpsync.pro
cd ..
%make -C libpsync
cp libpsync/libpsync.so.%{major}.0.0 .lib

cd .lib
ln -snf libpsync.so.%{major}.0.0 libpsync.so.%{major}.0
ln -snf libpsync.so.%{major}.0 libpsync.so.%{major}
ln -snf libpsync.so.%{major} libpsync.so
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

make -C syncd

%install
#make PREFIX=%buildroot%{_libdir} -C libcfg install
make INSTALL_ROOT=%buildroot -C liblcfg install
make INSTALL_ROOT=%buildroot -C libpsync install
make INSTALL_ROOT=%buildroot -C psyncconfig install
make INSTALL_ROOT=%buildroot -C psyncnotify install
make INSTALL_ROOT=%buildroot -C syncd install
make INSTALL_ROOT=%buildroot -C syncconfigapp install



%find_lang psyncconfig psyncnotify

%post
RES=`ls /home`
for i in $RES; do
    if [ -d /home/$i/.psyncclient ] ; then
        if [[ ! -f /home/$i/.psyncclient/sync.cfg || `stat -c %s /home/$i/.psyncclient/sync.cfg` == 413 ]] ; then
            array[0]=`[ -f /home/$i/.psyncclient/cfg/server/address ] && cat /home/$i/.psyncclient/cfg/server/address || echo 'sync1.mandrivasync.com' ` #Address
            array[1]=`[ -f /home/$i/.psyncclient/cfg/server/port ] && cat /home/$i/.psyncclient/cfg/server/port || echo '443' ` # Port
            array[2]=`[ -f /home/$i/.psyncclient/cfg/server/ssl ] && cat /home/$i/.psyncclient/cfg/server/ssl || echo 'yes'` # ssl
            array[3]=`[ -f /home/$i/.psyncclient/cfg/user/default_folder ] && cat /home/$i/.psyncclient/cfg/user/default_folder || echo ''` # Default folder
            array[4]='900' # Interval
#           array[5]=`[ -f /home/$i/.psyncclient/cfg/user/lastsync ] && cat /home/$i/.psyncclient/cfg/user/lastsync` # Last synchronization
            array[5]='' # Last sync
            array[6]=`[ -f /home/$i/.psyncclient/cfg/user/login ] && cat /home/$i/.psyncclient/cfg/user/login || echo ''` # Login
            array[7]=`[ -f /home/$i/.psyncclient/cfg/user/password ] && cat /home/$i/.psyncclient/cfg/user/password || echo '' ` # Password
            array[8]=`[ -f /home/$i/.psyncclient/cfg/user/show_tray_icon ] && cat /home/$i/.psyncclient/cfg/user/show_tray_icon || echo '2'` # Tray icon
            array[9]=`[ -f /home/$i/.psyncclient/cfg/user/sync_is ] && cat /home/$i/.psyncclient/cfg/user/sync_is || echo '0' ` # Sync_is
            array[10]='10' # Timer

#            find /home/$i/.psyncclient/ ! -regex '.*\(.psyncclient.*/\|sync.cfg\)' -delete
            cp -rn /etc/skel/.psyncclient/* /home/$i/.psyncclient/
            find /home/$i/.psyncclient/ ! -regex '.*\(.psyncclient.*/\|sync.cfg\)' -delete
            owner=`stat -c %U /home/$i/.psyncclient`
            group=`stat -c %G /home/$i/.psyncclient`
            chown $owner:$group /home/$i/.psyncclient/* -R
            mkdir -p /home/$i/.sync-unresolved
            chown $owner:$group /home/$i/.sync-unresolved

            
            sed -i -e "s/address = \"sync1.mandrivasync.com\";/address = \"${array[0]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/port = \"443\";/port = \"${array[1]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/ssl = \"yes\";/ssl = \"${array[2]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/sync_is = 0;/sync_is = ${array[9]};/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/interval = 0;/interval = ${array[4]};/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/default_folder = \"\";/default_folder = \"${array[3]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/login = \"\";/login = \"${array[6]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/password = \"\";/password = \"${array[7]}\";/" /home/$i/.psyncclient/sync.cfg
            sed -i -e "s/show_tray_icon = 2;/show_tray_icon = ${array[8]};/" /home/$i/.psyncclient/sync.cfg
#           echo 'works'
        else
            find /home/$i/.psyncclient/* ! -regex '.*\(.psyncclient.*/\|sync.cfg\)' -delete
        fi
    fi
done