%bcond_with                bootstrap
%define section            free
%define gcj_support        1

Name:           jflex
Version:        1.4.1
Release:        19
Epoch:          0
Summary:        A Lexical Analyzer Generator for Java
License:        GPL
Group:          Development/Java
Source0:        http://www.jflex.de/jflex-1.4.1.tar.bz2
Source1:        jflex.script
Source2:        jflex-1.4.1-generated-files.tar.bz2
Patch0:         jflex-javac-no-target.patch
Patch1:         jflex-no-cup-no-jflex.patch
Patch2:         jflex-classpath.patch
Patch3:         jflex-cup-anttask.patch
Patch4:         jflex-byaccj-utl.patch
URL:            http://www.jflex.de/
Requires:       java_cup
Requires:       jpackage-utils
BuildRequires:  ant
BuildRequires:  java_cup
BuildRequires:  locales-en
%if %without bootstrap
BuildRequires:  jflex
%endif
BuildRequires:  java-rpmbuild
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
JFlex is a lexical analyzer generator for Java written in Java. It is 
also a rewrite of the very useful tool JLex which was developed by 
Elliot Berk at Princeton University. As Vern Paxson states for his C/C++ 
tool flex: they do not share any code though.

Design goals The main design goals of JFlex are:

    * Full unicode support
    * Fast generated scanners
    * Fast scanner generation
    * Convenient specification syntax
    * Platfo%{__rm} independence
    * JLex compatibility

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{__rm} -rf src/java_cup
find . -name '*.jar' | xargs -t %{__rm}
%patch0 -p1
%if %with bootstrap
%setup -q -T -D -a 2
%patch1 -p1
%else
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif

%build
export LC_ALL=ISO-8859-1
pushd src
%if %without bootstrap
export CLASSPATH=$(build-classpath java-cup junit jflex)
%else
export CLASSPATH=$(build-classpath java-cup junit)
%endif
export OPT_JAR_LIST=
%if %without bootstrap
%ant realclean
%endif
%ant jar
%{__mkdir_p} ../dist/docs/api
%{javadoc} -d ../dist/docs/api `find . -type f -name "*.java"`
popd

%install
# jar
%{__mkdir_p} %{buildroot}%{_javadir}
%{__install} -m 644 lib/JFlex.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# compatibility symlink
(cd %{buildroot}%{_javadir} && %{__ln_s} jflex.jar JFlex.jar)
# javadoc
%{__mkdir_p} 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_bindir}/jflex

%{__perl} -pi -e 's/\r$//g' examples/standalone/sample.inp

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc COPYRIGHT doc examples src/README src/changelog
%attr(0755,root,root) %{_bindir}/jflex
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/JFlex.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-16mdv2011.0
+ Revision: 665825
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-15mdv2011.0
+ Revision: 606081
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.4.1-14mdv2010.1
+ Revision: 523084
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.4.1-13mdv2010.0
+ Revision: 425460
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0:1.4.1-12mdv2009.0
+ Revision: 221710
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.1-11mdv2008.1
+ Revision: 120941
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.4.1-10mdv2008.0
+ Revision: 87433
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.4.1-9mdv2008.0
+ Revision: 82536
- update to new version


* Wed Nov 08 2006 David Walluck <walluck@mandriva.org>
+ 2006-11-08 04:53:36 (78038)
- BuildRequires: jflex for non-bootstrap
- disable bootstrap

* Tue Nov 07 2006 David Walluck <walluck@mandriva.org> 1.4.1-6mdv2007.1
+ 2006-11-07 12:12:56 (77050)
- fix some (Build)Requires
- enable bootstrap
- Import jflex

* Sun Sep 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.1-4mdv2007.0
- fix build by removing included java_cup sources

* Sun Sep 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.1-3mdv2007.0
- don't clean generated files before build (fails)
- add byaccj url fix from Debian
- remove jflex dir from $RPM_BUILD_DIR

* Sun Sep 10 2006 David Walluck <walluck@mandriva.org> 0:1.4.1-2mdv2007.0
- clean build environment

* Sat Sep 09 2006 David Walluck <walluck@mandriva.org> 0:1.4.1-1mdv2007.0
- release

