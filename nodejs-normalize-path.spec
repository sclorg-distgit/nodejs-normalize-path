%{?scl:%scl_package nodejs-%{modname}}
%{!?scl:%global pkg_name %{name}}

%global modname normalize-path
%global enable_tests 0

%if ! ( 0%{?fedora} || 0%{?rhel} >= 7 )
%{?nodejs_find_provides_and_requires}
%global nodejs_arches %{ix86} x86_64 %{arm}
%endif

Name:           %{?scl_prefix}nodejs-%{modname}
Version:        2.0.1
Release:        2%{?dist}
Summary:        Nodejs library for normalizing filesystem paths
License:        MIT
URL:            https://github.com/jonschlinkert/normalize-path
# Upstream does not want to include tests in the npm tarballs, 
# so we use a Github snapshot instead.
# https://github.com/jonschlinkert/normalize-path/issues/2#issuecomment-72331596
#Source0:        http://registry.npmjs.org/%{modname}/-/%{modname}-%{version}.tgz
%global commit 3ad522d516a41c4f4212c8a4bd5c8005ef62b382
Source0:        https://github.com/jonschlinkert/%{modname}/archive/%{commit}/%{modname}-%{version}.tar.gz
BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch
BuildRequires:  nodejs010-runtime

%if 0%{?enable_tests}
BuildRequires:  %{?scl_prefix}mocha
BuildRequires:  %{?scl_prefix}npm(minimist)
BuildRequires:  %{?scl_prefix}npm(should)
BuildRequires:  /usr/bin/npm
%endif

%description
Normalize file path slashes to be unix-like forward slashes, regardless of OS 
(since in reality Windows doesn't care about slash direction anyway). Also 
condenses repeat slashes to a single slash and removes and trailing slashes.

%prep
%setup -q -n %{modname}-%{commit}

%build
# nothing to do

%if 0%{?enable_tests}

%check
%nodejs_symlink_deps --check
npm test
%endif

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{modname}
cp -pr package.json index.js \
    %{buildroot}%{nodejs_sitelib}/%{modname}/

%files
%{!?_licensedir:%global license %doc}
%doc README.md
%license LICENSE
%{nodejs_sitelib}/%{modname}

%changelog
* Mon Jan 11 2016 Tomas Hrcka <thrcka@redhat.com> - 2.0.1-2
- Enable scl macros

* Mon Nov 30 2015 Dan Callaghan <dcallagh@redhat.com> - 2.0.1-1
- upstream bug fix release 2.0.1: no longer strips leading ./

* Wed Nov 04 2015 Dan Callaghan <dcallagh@redhat.com> - 2.0.0-2
- added missing BR on minimist

* Wed Nov 04 2015 Dan Callaghan <dcallagh@redhat.com> - 2.0.0-1
- upstream release 2.0.0

* Tue Sep 01 2015 Dan Callaghan <dcallagh@redhat.com> - 1.0.0-1
- upstream release 1.0.0: paths are no longer forced to lower case

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 12 2014 Dan Callaghan <dcallagh@redhat.com> - 0.3.0-1
- upstream release 0.3.0

* Sun Oct 12 2014 Dan Callaghan <dcallagh@redhat.com> - 0.1.1-1
- initial version