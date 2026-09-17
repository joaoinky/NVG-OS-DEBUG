from pathlib import Path
import shutil, tempfile

root = Path.cwd()
dest = Path(tempfile.mkdtemp(prefix='nvg-audit-rust-')) / 'rust'
shutil.copytree(root / 'rust', dest, dirs_exist_ok=True, ignore=shutil.ignore_patterns('target', '.git'))

installer = r'''

#[cfg(test)]
mod auditoria_20260915 {
    use super::*;
    use crate::app::{Field, Picker, Screen};

    #[test]
    fn manual_aceita_particao_da_midia_live() {
        let mut a = crate::app::testes::app();
        a.modo = crate::app::Modo::Mbn;
        a.screen = Screen::Disk;
        a.mode = PartMode::Manual;
        let live = a.disks.iter().find(|d| d.is_live_media).unwrap().partitions[0].path.clone();
        assert!(a.manual_root.items.iter().any(|s| s.starts_with(&live)));
        a.manual_root = Picker::new(vec![live.clone()], &live);
        a.manual_esp = Picker::new(vec!["/dev/nvme0n1p1".into()], "/dev/nvme0n1p1");
        assert!(a.validate().is_ok());
        let p = Plan::from_app(&a);
        assert!(p.validate_before_install().is_ok());
        assert_eq!(p.manual_root, live);
        assert!(p.format_root);
        println!("CONFIRMADO: raiz da mídia Live aceita com formatação habilitada");
    }

    #[test]
    fn manual_aceita_raiz_esp_home_iguais_e_pequenos() {
        let mut a = crate::app::testes::app();
        a.screen = Screen::Disk;
        a.mode = PartMode::Manual;
        let part = a.disks[1].partitions[0].path.clone(); // ESP vfat de 512 MiB
        a.manual_root = Picker::new(vec![part.clone()], &part);
        a.manual_esp = Picker::new(vec![part.clone()], &part);
        a.manual_home = Picker::new(vec![part.clone()], &part);
        assert!(a.validate().is_ok());
        let p = Plan::from_app(&a);
        assert!(p.validate_before_install().is_ok());
        assert_eq!(p.manual_root, p.manual_esp);
        assert_eq!(p.manual_root, p.manual_home);
        println!("CONFIRMADO: ESP vfat de 512 MiB aceita simultaneamente como raiz formatada, ESP e home");
    }

    #[test]
    fn contas_reservadas_passam_no_preflight() {
        let mut a = crate::app::testes::app();
        a.screen = Screen::Account;
        for nome in ["root".to_string(), "daemon".to_string()] {
            a.username = Field::new(&nome);
            assert!(a.validate().is_ok());
            assert!(Plan::from_app(&a).validate_before_install().is_ok());
            println!("CONFIRMADO: usuário aceito no preflight: {nome}");
        }
    }
}
'''
with (dest/'nvg-installer/src/install.rs').open('a') as f:
    f.write(installer)

library = r'''
use nvg_nostr::{chave, cofre::Cofre, configs, pacote};
use std::{path::PathBuf, process::Command};

fn area(name: &str) -> PathBuf {
    let p = std::env::temp_dir().join(format!("nvg-audit-{}-{name}", std::process::id()));
    std::fs::create_dir_all(&p).unwrap();
    p
}

fn arquivo_tar(base: &std::path::Path, names: &[&str]) -> Vec<u8> {
    let p = Command::new("tar").args(["--zstd", "-cf", "-", "-C"])
        .arg(base).args(names).output().unwrap();
    assert!(p.status.success());
    p.stdout
}

#[test]
fn auditoria_envelope_nao_autenticado_causa_panic() {
    let k = chave::Keys::generate();
    let e = r#"{"v":1,"alg":"nip44-v2-blocos","bruto":18446744073709551615,"sha256":"","blocos":[]}"#;
    assert!(std::panic::catch_unwind(|| configs::decifrar(&k, e)).is_err());
    println!("CONFIRMADO: capacity overflow antes de decifrar/autenticar qualquer bloco");
}

#[test]
fn auditoria_instalador_extrai_arquivo_fora_da_lista() {
    let p = area("restaura");
    let src = p.join("origem");
    let dst = p.join("home");
    std::fs::create_dir_all(src.join(".ssh")).unwrap();
    std::fs::write(src.join(".ssh/authorized_keys"), "APENAS-MARCADOR-DE-TESTE").unwrap();
    let tar = arquivo_tar(&src, &[".ssh"]);
    assert!(!pacote::na_lista(".ssh/authorized_keys"));
    configs::desempacotar(&dst, &tar).unwrap();
    assert_eq!(std::fs::read_to_string(dst.join(".ssh/authorized_keys")).unwrap(), "APENAS-MARCADOR-DE-TESTE");
    println!("CONFIRMADO: caminho fora da lista escrito pela função usada no instalador");
    std::fs::remove_dir_all(p).unwrap();
}

#[test]
fn auditoria_aplicacao_do_cofre_segue_link_no_home() {
    assert!(!nvg_nostr::cofre::sou_root(), "execute como usuário comum");
    let p = area("cofre-link");
    std::env::set_var("NVG_COFRE", p.join("cofre"));
    let c = Cofre::abrir_escrita("auditoria descartável").unwrap();
    let src = p.join("origem");
    let home = p.join("home");
    let outside = p.join("fora-do-home");
    std::fs::create_dir_all(src.join(".config")).unwrap();
    std::fs::create_dir_all(&home).unwrap();
    std::fs::create_dir_all(&outside).unwrap();
    std::fs::write(src.join(".config/kwinrc"), "NOVO").unwrap();
    std::fs::write(outside.join("kwinrc"), "ANTIGO").unwrap();
    std::os::unix::fs::symlink(&outside, home.join(".config")).unwrap();
    pacote::instalar(&c, &arquivo_tar(&src, &[".config"])).unwrap();
    pacote::aplicar(&c, &home, 1000, 1000).unwrap();
    assert_eq!(std::fs::read_to_string(outside.join("kwinrc")).unwrap(), "NOVO");
    // O temporário previsível também segue link, mesmo com .config real.
    std::fs::remove_file(home.join(".config")).unwrap();
    std::fs::create_dir(home.join(".config")).unwrap();
    let victim = outside.join("arquivo-sentinela");
    std::fs::write(&victim, "ANTIGO").unwrap();
    std::os::unix::fs::symlink(&victim, home.join(".config/kwinrc.nvg-tmp")).unwrap();
    pacote::aplicar(&c, &home, 1000, 1000).unwrap();
    assert_eq!(std::fs::read_to_string(&victim).unwrap(), "NOVO");
    println!("CONFIRMADO: diretório e temporário simbólicos permitem escrita fora do home");
    drop(c);
    std::fs::remove_dir_all(p).unwrap();
}
'''
(dest/'nvg-nostr/tests/auditoria_20260915.rs').write_text(library)
print(dest)
