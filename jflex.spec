
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Name:		jflex
Version:	1.4.3
Release:	16.0
Summary:	javapackages-bootstrap packages
License:	GPLv3+
Source0:	jflex-1.4.3-16.0-omv2014.0.noarch.rpm
URL:		https://abf.rosalinux.ru/openmandriva/jflex
Summary:	jflex bootstrap version
Requires:	javapackages-bootstrap
Requires:	emacs
Requires:	java
Requires:	java_cup
Requires:	jpackage-utils
Provides:	jflex = 0:1.4.3-16.0:2014.0
Provides:	mvn(de.jflex:jflex) = 1.4.3

%description
jflex bootstrap version.

%files		-n jflex
/usr/bin/jflex
/usr/share/applications/jflex.desktop
/usr/share/doc/jflex
/usr/share/doc/jflex/COPYRIGHT
/usr/share/doc/jflex/doc
/usr/share/doc/jflex/doc/COPYRIGHT
/usr/share/doc/jflex/doc/crossref.png
/usr/share/doc/jflex/doc/footnote.png
/usr/share/doc/jflex/doc/jflex_anttask.html
/usr/share/doc/jflex/doc/logo.png
/usr/share/doc/jflex/doc/manual.css
/usr/share/doc/jflex/doc/manual.html
/usr/share/doc/jflex/doc/manual.pdf
/usr/share/doc/jflex/doc/manual.ps.gz
/usr/share/java/JFlex.jar
/usr/share/java/jflex.jar
/usr/share/man/man1/jflex.1.gz
/usr/share/maven-fragments/jflex
/usr/share/maven-poms/JPP-jflex.pom
/usr/share/pixmaps/jflex.png

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
