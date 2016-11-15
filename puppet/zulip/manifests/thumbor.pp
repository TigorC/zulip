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

  $aws_access_key = zulipsecret("secrets", "s3_key", '')
  $aws_secret_access_key = zulipsecret("secrets", "s3_secret_key", '')
  $aws_region = zulipsecret("secrets", "s3_region", 'us-east-1')

  file { "/home/zulip/.aws/config":
    ensure => file,
    owner  => "zulip",
    group  => "zulip",
    mode => 644,
    content => template("zulip/aws_config.template.erb"),
  }

  file { "/home/zulip/.aws/credentials":
    ensure => file,
    owner  => "zulip",
    group  => "zulip",
    mode => 644,
    content => template("zulip/aws_credentials.template.erb"),
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
