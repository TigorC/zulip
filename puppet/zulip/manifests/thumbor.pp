# Class: zulip::thumbor
#
#
class zulip::thumbor {
  $thumbor_packages = [
    "ffmpeg",
    "libssl-dev",
    "libcurl4-openssl-dev",
    "libjpeg-dev",
    "libpng-dev",
    "libtiff-dev",
    "libjasper-dev",
    "libgtk2.0-dev",
    "libwebp-dev",
    "webp",
    "gifsicle"
  ]

  package { $thumbor_packages: ensure => "installed" }

  file { '/srv/thumbor':
    ensure => 'directory',
  }

  file { "/srv/thumbor/thumbor.conf":
    ensure => present,
    source  => "/srv/zulip/zthumbor/thumbor.conf"
  }

  file { "/etc/supervisor/conf.d/thumbor.conf":
    require => Package[supervisor],
    ensure => file,
    owner => "root",
    group => "root",
    mode => 644,
    source => "puppet:///modules/zulip/supervisor/conf.d/thumbor.conf",
    notify => Service["supervisor"],
  }
}
