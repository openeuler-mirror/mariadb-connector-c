Name:           mariadb-connector-c
Version:        3.0.6
Release:        3
Summary:        MariaDB connector library in C
License:        LGPLv2+
Url:            https://github.com/MariaDB/mariadb-connector-c
Source:         https://downloads.mariadb.org/interstitial/connector-c-%{version}/mariadb-connector-c-%{version}-src.tar.gz
#Source2-3 come from fedora29
Source2:        my.cnf
Source3:        client.cnf

BuildRequires:  libcurl-devel zlib-devel openssl-devel
BuildRequires:  cmake git
Provides:       %{name}-config%{?_isa} %{name}-config
Obsoletes:      %{name}-config

%description
This package is used for connecting C/C++ programs to MariaDB and
MySQL database.



%package devel
Summary:        Mariadb-connector-c library and header files
BuildRequires:  multilib-rpm-config
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel

%description devel
This package includes library and header files for development.

%prep
%autosetup -n %{name}-%{version}-src -p1 -S git

%build
%cmake . \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_SYSTEM_PROCESSOR="%{_arch}" \
       -DMARIADB_UNIX_ADDR=%{_sharedstatedir}/mysql/mysql.sock \
       -DMARIADB_PORT=3306 \
       -DWITH_EXTERNAL_ZLIB=YES \
       -DWITH_SSL=OPENSSL \
       -DWITH_MYSQLCOMPAT=ON \
       -DINSTALL_LAYOUT=RPM \
       -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
       -DINSTALL_BINDIR="bin" \
       -DINSTALL_LIBDIR="%{_lib}" \
       -DINSTALL_INCLUDEDIR="include/mysql" \
       -DINSTALL_PLUGINDIR="%{_lib}/mariadb/plugin" \
       -DWITH_UNITTEST=ON
%make_build



%install
%make_install
%multilib_fix_c_header --file %{_includedir}/mysql/mariadb_version.h
ln -s mariadb_config %{buildroot}%{_bindir}/mysql_config
ln -s mariadb_version.h %{buildroot}%{_includedir}/mysql/mysql_version.h
mkdir -p %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}%{_sysconfdir}/my.cnf.d
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/my.cnf
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf

%check
%{buildroot}%{_bindir}/mariadb_config
pushd unittest/libmariadb/
ctest || :
popd

%pretrans -p <lua>
path = "%{_libdir}/mariadb"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end
path = "%{_libdir}/mysql"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end

%files
%doc README
%license COPYING.LIB
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%dir %{_libdir}/mariadb
%{_libdir}/libmariadb.so.*
%{_libdir}/mariadb/plugin/*
%exclude %{_libdir}/*.a

%files devel
%{_bindir}/mariadb_config
%{_bindir}/mysql_config
%{_includedir}/mysql/*
%{_libdir}/*.so

%changelog
* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 3.0.6-3
- Package init

