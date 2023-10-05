class web_static {
  $nginx_package_name = 'nginx'
  $web_static_dirs = ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']
  $web_owner = 'ubuntu'
  $web_group = 'ubuntu'
  $nginx_config_file = '/etc/nginx/sites-available/default'

  package { $nginx_package_name:
    ensure => installed,
  }

  file { $web_static_dirs:
    ensure => directory,
    owner  => $web_owner,
    group  => $web_group,
    mode   => '0755',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => '<html><head></head><body>This is a test</body></html>',
    owner   => $web_owner,
    group   => $web_group,
    mode    => '0644',
  }

  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test',
    force  => true,
    owner  => $web_owner,
    group  => $web_group,
  }

  exec { 'update_nginx_config':
    command     => "sed -i 's|^\tlocation / {|\\tlocation /hbnb_static/ {\\n\\t\\talias /data/web_static/current/;\\n\\t}\\n\\n\\tlocation / {|' ${nginx_config_file}",
    path        => ['/bin', '/usr/bin'],
    refreshonly => true,
    subscribe   => File['/data/web_static/current'],
  }

  service { 'nginx':
    ensure     => running,
    enable     => true,
    subscribe  => Exec['update_nginx_config'],
  }
}

include web_static

