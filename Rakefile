require 'bundler/setup'

require 'docker'
require 'minigit'

ENV['INTERNAL_REGISTRY'] ||= ENV['REGISTRY'] || 'localhost:5000'
ENV['PUBLIC_REGISTRY'] ||= ENV['REGISTRY'] || '3ofcoins'
ENV['REGISTRY'] ||= 'localhost:5001'
ENV['MAINTAINER'] ||= 'Maciej Pasternacki <maciej@3ofcoins.net>'

if ENV['DOCKER_USERNAME'] || ENV['DOCKER_EMAIL'] || ENV['DOCKER_PASSWORD']
  unless ENV['DOCKER_USERNAME'] && ENV['DOCKER_EMAIL'] && ENV['DOCKER_PASSWORD']
    raise "Need all of DOCKER_USERNAME, DOCKER_EMAIL, DOCKER_PASSWORD"
  end
  puts "# Authenticating to the Docker index as #{ENV['DOCKER_USERNAME']}"
  Docker.authenticate! 'username' => ENV['DOCKER_USERNAME'],
                       'email' => ENV['DOCKER_EMAIL'],
                       'password' => ENV['DOCKER_PASSWORD']
else
  Docker.creds = {}
end

class DockerImageTask < Rake::Task
  include FileUtils

  def initialize(*args)
    super
    enhance(&:build!)
    repo_task = Rake::Task.define_task(repository => self)
    repo_task.comment = tagged
  end

  def build!(task=nil)
    puts "# Building #{self}"
    if ENV['COMPILE']
      Dir.chdir(name) do
        sh "#{File.join(File.dirname(__FILE__), 'script/docker-compile.pl')} | tee compile.log"
      end
      iid = Array(File.read(File.join(name, 'compile.log')).lines).last.strip
      raise "Suspicious image ID #{iid}" unless iid =~ /^[0-9a-f]{6,128}$/
      @image = Docker::Image.all.find { |img| img.id.start_with?(iid) }
    else
      @image = Docker::Image.build_from_dir(name)
    end

    if tag != ''
      puts "# tag #{repository}:#{tag}"
      image.tag('repo' => repository, 'tag' => tag)
    end

    puts "# tag #{repository}:latest"
    image.tag('repo' => repository)

    if ENV['COMPILE']
      puts "# push #{repository}"
      image.info['Repository'] = repository
      image.push
    end
  end

  def needed?
    dirty? || !image
  end

  def image
    @image ||= Docker::Image.all.find { |img| "#{img.info['Repository']}:#{img.info['Tag']}" == tagged }
  end

  def tag
    @docker_tag ||= sha1
  end

  def registry
    case name
    when /^internal\// then ENV['INTERNAL_REGISTRY']
    when /^public\//   then ENV['PUBLIC_REGISTRY']
    else ENV['REGISTRY']
    end
  end

  def repository
    "#{registry}/#{File.basename(name)}"
  end

  def tagged
    "#{repository}:#{tag}"
  end

  def dockerfile
    "#{name}/Dockerfile"
  end

  def sha1
    git.rev_list({max_count: 1}, 'HEAD', '--', name).strip
  end

  def dirty?
    !git.status({porcelain: true}, name).empty?
  end

  def git
    @git ||= MiniGit::Capturing.new(name)
  end
end

desc 'All Docker images'
task :images

Dir['internal/Dockerfile', 'public/Dockerfile'].each do |df|
  deps = [ file(df) ]
  from = File.read(df).lines.grep(/^\s*from\s+/i).first.strip.split(nil, 2)[1]
  deps << from if from.start_with?(ENV['REGISTRY']) || from.start_with?(ENV['PUBLIC_REGISTRY'])
  task :images => DockerImageTask.define_task(File::dirname(df) => file(df))
end

task :pry do
  require 'pry'
  binding.pry
end
