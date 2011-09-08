Summary:       MandrivaSync client
Name:          psyncclient
Version:       0.1
Release:       14
License:       GPLv2
Group:         Graphical desktop/KDE
Source:        %{name}-%{version}.tar.gz
Requires:      %{_lib}psync = %{version}-%{release}
BuildRequires: qt4-devel
BuildRequires: kdelibs4-devel
BuildRequires: libuuid-devel
BuildRequires: libneon-devel

%description
MandrivaSync client

%files -f psyncconfig.lang
%{_bindir}/*
%{_sysconfdir}/skel/.psyncclient
%{_sysconfdir}/skel/sync-unresolved
%{_datadir}/autostart/psyncnotify.desktop
%{_datadir}/autostart/psyncd.desktop
%{_datadir}/icons/default.kde4/128x128/apps/sync.png
%{_datadir}/icons/default.kde4/64x64/apps/sync.png
%{_datadir}/icons/default.kde4/48x48/apps/sync.png
%{_datadir}/icons/default.kde4/32x32/apps/sync.png
%{_datadir}/icons/default.kde4/22x22/apps/sync.png
%{_datadir}/icons/default.kde4/16x16/apps/sync.png
%{_datadir}/kde4/services/kcm_sync.desktop
%{_libdir}/kde4/kcm_sync.so

#-------------------------------------------------------------------------------

%define major_psync 1
%define libpsync %mklibname psync
      
%package -n %libpsync
Group:          Graphical desktop/KDE
Summary:        MandrivaSync client
Obsoletes:	%{_lib}psyncipc1,%{_lib}psync1
      
%description -n %libpsync
psync library

%files -n %libpsync
%{_libdir}/libpsync.so.%{major_psync}*
%{_libdir}/libcfg.so
%{_libdir}/libpsync.so

#-------------------------------------------------------------------------------

%define develname %mklibname -d psync

%package -n     %develname
Group:          Development/KDE and Qt
Summary:        %name developement files
Provides:       %name-devel = %version-%release
Requires:       %libpsync = %version-%release
Obsoletes:	libpsyncipc-devel

%description -n %develname
Development files for %name .

%files -n %develname

%{_libdir}/libcfg.a
%{_includedir}/psync/*

#--------------------------------------------------------------------

%prep
%setup -c 

%build


sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libpsync/libpsync.pro
sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./psyncconfig/psyncconfig.pro


mkdir -p .lib
%make -C libcfg
cp libcfg/libcfg.so .lib

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

cd psyncconfig
qmake psyncconfig.pro
%make
cd ..

cd psyncnotify
qmake psyncnotify.pro
%make
cd ..

make -C syncd

%install
make PREFIX=%buildroot%{_libdir} -C libcfg install
make INSTALL_ROOT=%buildroot -C libpsync install
make INSTALL_ROOT=%buildroot -C psyncconfig install
make INSTALL_ROOT=%buildroot -C psyncnotify install
make INSTALL_ROOT=%buildroot -C syncd install
                           
%find_lang psyncconfig psyncnotify

%post 
RES=`ls /home`
for i in $RES; do
    if [ -d /home/$i/.psyncclient ] ; then
        find /home/$i/.psyncclient/ ! -regex '.*\(psyncclient.*/\|cfg\|cfg/user\|login\|password\)' -delete
	cp -r /etc/skel/.psyncclient/* /home/$i/.psyncclient/
        owner=`stat -c %U /home/$i/.psyncclient`
        group=`stat -c %G /home/$i/.psyncclient`
        chown $owner:$group /home/$i/.psyncclient/* -R
        mkdir -p /home/$i/sync-unresolved
        chown $owner:$group /home/$i/sync-unresolved
    fi
done
                           

