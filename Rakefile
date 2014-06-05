require 'bundler/setup'

require 'docker'
require 'etcd'
require 'minigit'

$git = MiniGit::Capturing.new(__FILE__)
$etcd = Etcd.client(
  host: ENV['ETCD_HOST'] || '127.0.0.1',
  port: (ENV['ETCD_PORT'] || 4001).to_i)

ENV['ETCD_PREFIX'] ||= '/3ofcoins/docker-images'
DOCKER_REBASE = File.join(Dir.getwd, 'script/docker-rebase.rb')
GIT_BRANCH = ENV['GIT_BRANCH'] ? ENV['GIT_BRANCH'].sub(/^origin\//, '') :
  $git.rev_parse({ abbrev_ref: true }, 'HEAD').strip

class DockerImageTask < Rake::Task
  include Rake::FileUtilsExt    # for #sh

  PULL = Hash.new do |h, k|
    h[k] = Rake::Task.define_task("docker:pull:#{k}") do
      $stdout.write "Pulling #{k} ... "
      $stdout.flush
      image, tag = k.split(':')
      tag ||= 'latest'
      img = Docker::Image.create(fromImage: image, tag: tag)
      $stdout.puts img.id
    end
  end

  def initialize(*args, &block)
    super
    enhance [ PULL[base_image_name] ], &:build!
  end

  def sha1
    @sha1 ||= $git.rev_list({max_count: 1}, 'HEAD', '--', name).strip
  end

  def etcd_key
    "#{ENV['ETCD_PREFIX']}/#{name}/built/sha1:#{sha1}"
  end

  def image_name(tag=nil)
    rv = "#{ENV['REGISTRY']}/#{File.basename(name)}"
    rv << ":#{tag}" if tag
    rv
  end

  def tag!(*tags)
    return unless ENV['REGISTRY']
    tags = self.tags if tags.empty?
    tags.each do |tag|
      sh "docker tag #{image_id} #{image_name(tag)}"
      sh "docker push #{image_name(tag)}"
    end
  end

  def tags
    @tags ||= begin
                rv = dockerfile
                  .map { |ln| ln =~ /^\s*\#\s*tag\s+/i && $'.split }
                  .compact
                  .flatten
                rv << GIT_BRANCH
                rv << 'latest' if GIT_BRANCH == 'master'
                rv
              end
  end

  def image_id
    @image_id ||= $etcd.get(etcd_key).value
  rescue Etcd::KeyNotFound
    nil
  end

  def image
    Docker::Image.get(image_id) if image_id
  end

  def save_id!
    $etcd.set(etcd_key, value: image_id)
  end

  def dockerfile
    @dockerfile ||= File.read(File.join(name, "Dockerfile"))
      .lines
      .map(&:strip)
  end

  def base_image_name
    @base_image_name ||= dockerfile
      .grep(/^\s*from\s/i)
      .first
      .sub(/^\s*from\s+/i, '')
  end

  def base_image
    Docker::Image.get(base_image_name)
  end

  def needed?
    image.nil? || image.info['parent'] != base_image.id
  end

  def build!(*)
    sh "ruby #{DOCKER_REBASE}#{' --verbose' if ENV['VERBOSE']} --save-id=#{self}/.image_id --build #{self}"
    @image_id = File.read("#{self}/.image_id")
    tag!
    save_id!
  end
end

def docker_image(path, &block)
  path = File.dirname(path) if File.basename(path) == 'Dockerfile'
  desc "docker build #{path}"
  DockerImageTask.define_task(path, &block)
end

desc 'All Docker images'
task :images

Dir['public/*/Dockerfile'].each { |df| task :images => docker_image(df) }

task :pry do
  require 'pry'
  binding.pry
end
