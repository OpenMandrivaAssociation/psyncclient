Summary:       ROSA Sync client
Name:          psyncclient
Version:       0.1
Release:       4
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

#-------------------------------------------------------------------------------

%define major_psyncipc  1
%define libpsyncipc %mklibname psyncipc %major_psyncipc
      
%package -n %libpsyncipc
Group:          Graphical desktop/KDE
Summary:        ROSA Sync client
      
%description -n %libpsyncipc
Qt Zeitgeist Library.

%files -n %libpsyncipc
%{_libdir}/libpsyncipc.so.%{major_psyncipc}*

#-------------------------------------------------------------------------------

%define develname %mklibname -d psyncipc

%package -n     %develname
Group:          Development/KDE and Qt
Summary:        %name developement files
Provides:       %name-devel = %version-%release
Requires:       %libpsyncipc = %version-%release

%description -n %develname
Development files for %name .

%files -n %develname

%{_libdir}/libcfg.so
%{_libdir}/libpsyncipc.so
%{_libdir}/libcfg.a

#--------------------------------------------------------------------

%prep
%setup -c 

%build


sed -i 's/\/usr\/lib/\/usr\/%_lib/' ./psyncipclibrary/psyncipclibrary/psyncipclibrary.pro


mkdir -p .lib
%make -C libcfg
cp libcfg/libcfg.so .lib

cd psyncipclibrary/psyncipclibrary
qmake psyncipclibrary.pro
cd ../..
%make -C psyncipclibrary/psyncipclibrary
cp psyncipclibrary/psyncipclibrary/libpsyncipc.so.1.0.0 .lib

cd .lib
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so.1.0
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so.1
ln -s libpsyncipc.so.1.0.0 libpsyncipc.so
cd ..

cd psyncconfig/psyncconfig
qmake psyncconfig.pro
%make
cd ../..

cd psyncnotify/psyncnotify
qmake psyncnotify.pro
%make
cd ../..

make -C syncd

%install
make PREFIX=%buildroot%{_libdir} -C libcfg install
make INSTALL_ROOT=%buildroot -C psyncipclibrary/psyncipclibrary install
make INSTALL_ROOT=%buildroot -C psyncconfig/psyncconfig install
make INSTALL_ROOT=%buildroot -C psyncnotify/psyncnotify install
make INSTALL_ROOT=%buildroot -C syncd install
                           
%find_lang psyncconfig psyncnotify

