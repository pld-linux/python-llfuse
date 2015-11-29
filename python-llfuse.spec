#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	llfuse
Summary:	Python bindings for the low level FUSE API
Name:		python-%{module}
Version:	0.40
Release:	5
License:	GPL v2
Group:		Libraries/Python
Source0:	https://python-llfuse.googlecode.com/files/llfuse-%{version}.tar.bz2
# Source0-md5:	bd8d07ddb6061ab03816e636efa37b5b
URL:		https://code.google.com/p/python-llfuse/
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	libfuse-devel >= 2.8.0
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for the low level FUSE API.

%package -n python3-%{module}
Summary:	Python bindings for the low level FUSE API
Group:		Libraries/Python

%description -n python3-%{module}
Python bindings for the low level FUSE API.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

# in case there are examples provided
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc Changes.txt
%dir %{py_sitedir}/llfuse
%{py_sitedir}/llfuse/*.py[co]
%attr(755,root,root) %{py_sitedir}/llfuse/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/llfuse-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc Changes.txt
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py*
%{py3_sitedir}/%{module}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{module}/capi*.so
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
