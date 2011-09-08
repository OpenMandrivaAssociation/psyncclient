Summary:       ROSA Sync client
Name:          psyncclient
Version:       0.1
Release:       9
License:       GPLv2
Group:         Graphical desktop/KDE
Source:        %{name}-%{version}.tar.gz
BuildRequires: qt4-devel
BuildRequires: kdelibs4-devel
BuildRequires: libuuid-devel

%description
ROSA Sync client

%files -f psyncconfig.lang
%{_bindir}/*
%{_sysconfdir}/skel/.psyncclient
%{_datadir}/autostart/psyncnotify.desktop
%{_datadir}/autostart/psyncd.desktop
%{_datadir}/icons/default.kde4/128x128/apps/2safe.png
%{_datadir}/kde4/services/kcm-2safe.desktop

#-------------------------------------------------------------------------------

%define major_psync 1
%define libpsync %mklibname psync %major_psync
      
%package -n %libpsync
Group:          Graphical desktop/KDE
Summary:        ROSA Sync client
Obsoletes:	libpsyncipc1
      
%description -n %libpsync
psync library

%files -n %libpsync
%{_libdir}/libpsync.so.%{major_psync}*

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

%{_libdir}/libcfg.so
%{_libdir}/libpsync.so
%{_libdir}/libcfg.a

#--------------------------------------------------------------------

%prep
%setup -c 

%build


sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./libpsync/libpsync.pro


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

