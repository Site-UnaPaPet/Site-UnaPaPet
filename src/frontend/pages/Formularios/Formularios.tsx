import { Link } from "react-router-dom";
import { ArrowRight, ClipboardList, FileText } from "lucide-react";

import filhotes from "@/assets/filhotes-formularios.webp";
import PageBanner from "@/components/layout/PageBanner";
import { Button } from "@/components/ui/button";

export default function Formularios() {
  return (
    <>
      <PageBanner
        titulo="Formulários"
        subtitulo="fonte de estudo teórico da veterinária"
        icone={<FileText />}
        ilustracao={<ClipboardList />}
      />

      <div className="mx-auto grid w-full max-w-7xl gap-8 px-4 py-8 sm:px-6 lg:grid-cols-[2fr_3fr] lg:items-center lg:gap-16 lg:px-14 lg:py-14">
        <img
          src={filhotes}
          alt="Três filhotes de cachorro"
          className="h-52 w-full rounded-2xl object-cover shadow-lg lg:aspect-square lg:h-auto"
        />
        <section aria-live="polite" className="min-w-0">
          <ul className="flex flex-col gap-4 lg:gap-5">
            <li
              key={'formulario Triagem Clínica'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Triagem Clínica</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:x:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/1.%20Triagem%20Cl%C3%ADnica/DEMANDAS%20-%20TRIAGEM%20CL%C3%8DNICA.xlsx?d=wcb744156d5474a2785a7f808da60c413&csf=1&web=1&e=3gchyB'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Triagem Clínica(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Manejo Sanitario'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Manejo Sanitário</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:x:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/2.%20Manejo%20Sanit%C3%A1rio/DEMANDAS%20-%20MANEJO%20SANIT%C3%81RIO.xlsx?d=wb4a860be3dcf452ebb345397d5c97ba7&csf=1&web=1&e=HJ7DhP'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Manejo Sanitário(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Clínica e Cirurgia'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Clínica e Cirurgia</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:x:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/3.%20Cl%C3%ADnica%20e%20Cirurgia/DEMANDAS%20-%20CL%C3%8DNICA%20E%20CIRURGIA.xlsx?d=w0a020655b4a448b4ab8d9d7db7fa7f49&csf=1&web=1&e=zE7JGn'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Clínica e Cirurgia(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Acolhimento e Adoção'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Acolhimento e Adoção</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:x:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/4.%20Acolhimento%20e%20Ado%C3%A7%C3%A3o/DEMANDAS%20-%20ACOLHIMENTO%20E%20ADO%C3%87%C3%83O.xlsx?d=wc4aef65010ec410c83701f47c68270b3&csf=1&web=1&e=0uBqrh'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Acolhimento e Adoção(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Banco de Dados'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Banco de Dados</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:f:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/5.%20Banco%20de%20%20Dados?d=w0d5032d9beff4cc6a6c27d8ade6b2ff2&csf=1&web=1&e=MsOqj7'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Banco de Dados(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Comunicação'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Comunicação</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:f:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/6.%20Comunica%C3%A7%C3%A3o?d=wcfdc3c5036c34bd5bd0c816153aac186&csf=1&web=1&e=W4jay0'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Comunicação(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
            <li
              key={'formulario Conforto e Bem-estar Animal'} 
              className="flex items-center justify-between gap-3 rounded-md bg-card px-4 py-4 text-card-foreground lg:px-6"
            >
              <span className="min-w-0 flex-1 text-center break-words lg:text-lg">Conforto e Bem-estar Animal</span>
              <Button asChild size="lg" className="shrink-0">
                <Link
                  to={'https://animaedu-my.sharepoint.com/:f:/r/personal/62612241_ulife_com_br/Documents/UnaP%C3%A1Pet/7.%20Conforto%20e%20Bem-estar%20%20Animal?d=w845f101a6ffb47389933b70ea7ee8054&csf=1&web=1&e=AwPntC'}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Acessar Conforto e Bem-estar Animal(abre em nova aba)`}
                >
                  Acessar <ArrowRight aria-hidden />
                </Link>
              </Button>
            </li>
          </ul>
        </section>
      </div>
    </>
  );
}
