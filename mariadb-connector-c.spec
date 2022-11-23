Name:           mariadb-connector-c
Version:        3.1.13
Release:        4
Summary:        MariaDB connector library in C
License:        LGPLv2+
URL:            https://github.com/MariaDB/mariadb-connector-c
Source0:        https://downloads.mariadb.com/Connectors/c/connector-c-%{version}/mariadb-connector-c-%{version}-src.tar.gz

Patch0001:	0001-CVE-2022-37434.patch
Patch0002:	0002-CVE-2022-37434.patch
Patch0003:      mariadb-connector-c-3.1.13-src-sw.patch

BuildRequires:  libcurl-devel zlib-devel openssl-devel
BuildRequires:  cmake gcc
Provides:       %{name}-config%{?_isa} %{name}-config
Obsoletes:      %{name}-config

%description
This package is used for connecting C/C++ programs to MariaDB and
MySQL database.



%package devel
Summary:        Mariadb-connector-c library and header files
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel

%description devel
This package includes library and header files for development.

%prep
%autosetup -n %{name}-%{version}-src -p1

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
ln -s mariadb_config %{buildroot}%{_bindir}/mysql_config
ln -s mariadb_version.h %{buildroot}%{_includedir}/mysql/mysql_version.h
mkdir -p %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}%{_sysconfdir}/my.cnf.d

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
%dir %{_sysconfdir}/my.cnf.d
%dir %{_libdir}/mariadb
%{_libdir}/libmariadb.so.*
%dir %{_libdir}/mariadb/plugin
%{_libdir}/mariadb/plugin/*
%exclude %{_libdir}/*.a

%files devel
%{_bindir}/mariadb_config
%{_bindir}/mysql_config
%dir %{_includedir}/mysql
%{_includedir}/mysql/*
%{_libdir}/*.so
%ifarch loongarch64
%{_prefix}/lib/pkgconfig/libmariadb.pc
%else
%{_libdir}/pkgconfig/libmariadb.pc
%endif

%changelog
* Wed Nov 23 2022 wuzx<wuzx1226@qq.com> - 3.1.13-4
- Add sw64 architecture

* Mon Nov 14 2022 zhaozhen <zhaozhen@loongson.cn> - 3.1.13-3
- Add loongarch support

* Mon Oct 10 2022 Jiangtian Feng <fengjiangtian@huawei.com> -3.1.13-2
- Type:CVE
- CVE:CVE-2022-37434
- SUG:NA
- DESC: fix CVE-2022-37434
- fix CVE-2022-37434

* Thu Dec 9 2021 yanglongkang <yanglongkang@huawei.com> - 3.1.13-1
- update package to 3.1.13

* Tue Jun 29 2021 zhouwenpei <zhouwenpei1@huawei.com> - 3.0.6-8
- add buildrequire gcc

* Tue Nov 10 2020 yanglongkang <yanglongkang@huawei.com> - 3.0.6-7
- Temporarily roll back the version 3.0.6 to resolve the conflict

* Tue Jul 21 2020 jixinjie <jixinjie@huawei.com> - 3.1.9-1
- update package to 3.1.9

* Mon Jan 13 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.0.6-6
- Type:enhance
- ID:NA
- SUG:restart
- DESC:repackaged

* Wed Jan 8 2020 openEuler Buildteam <buildteam@openeuler.org> - 3.0.6-5
- Type:enhance
- ID:NA
- SUG:restart
- DESC:repackaged

* Sun Dec 29 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.0.6-4
- Type:bugfix
- ID:NA
- SUG:restart
- DESC:add the needed dir

* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 3.0.6-3
- Package init

